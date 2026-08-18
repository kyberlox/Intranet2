<template>
<div class="modal__text__content modal__text__content--user-points">
    <div v-if="featureFlags.transactions"
         class="points-transactions__tabs"
         role="tablist"
         aria-label="Операции с баллами">
        <button class="points-transactions__tab"
                :class="{ 'points-transactions__tab--active': activeTab === 'history' }"
                type="button"
                role="tab"
                :aria-selected="activeTab === 'history'"
                @click="activeTab = 'history'">
            История
        </button>
        <button class="points-transactions__tab"
                :class="{ 'points-transactions__tab--active': activeTab === 'send' }"
                type="button"
                role="tab"
                :aria-selected="activeTab === 'send'"
                @click="activeTab = 'send'">
            Отправить баллы
        </button>
    </div>

    <div v-if="activeTab === 'history'">
        <PointsInfoTable historyType="addition" />
        <div class="modal__text__content__points-info__list">
            <a href="/about/capitalEmk/about"
               target="_blank"
               class="link">
                За что начисляют
            </a>
        </div>
    </div>

    <form v-else-if="featureFlags.transactions"
          class="points-transactions__form"
          @submit.prevent="sendPoints">
        <div class="admin-element-inner__field-content">
            <p class="admin-element-inner__field-title fs-l">Получатель</p>
            <template v-if="!selectedUser">
                <input v-model.trim="searchQuery"
                       class="admin-element-inner__input fs-m"
                       type="search"
                       autocomplete="off"
                       placeholder="Начните вводить имя сотрудника" />
                <SearchList v-if="usersList.length"
                            :searchList="usersList"
                            @pick="selectUser" />
                <span v-else-if="searchQuery && !isSearching"
                      class="points-transactions__hint">
                    Сотрудники не найдены
                </span>
                <span v-if="isSearching"
                      class="points-transactions__hint">
                    Поиск…
                </span>
            </template>
            <div v-else
                 class="points-transactions__recipient">
                <span>{{ selectedUser.name }}</span>
                <button type="button"
                        class="link points-transactions__recipient-change"
                        @click="clearSelectedUser">
                    Изменить
                </button>
            </div>
        </div>

        <div class="admin-element-inner__field-content">
            <label for="peer-transaction-amount"
                   class="admin-element-inner__field-title fs-l">
                Количество баллов
            </label>
            <input id="peer-transaction-amount"
                   v-model.number="amount"
                   class="admin-element-inner__input fs-m"
                   type="number"
                   min="1"
                   step="1"
                   :max="currentScore"
                   placeholder="Введите количество" />
        </div>

        <div class="admin-element-inner__field-content">
            <label for="peer-transaction-message"
                   class="admin-element-inner__field-title fs-l">
                Сообщение
            </label>
            <textarea id="peer-transaction-message"
                      v-model.trim="message"
                      class="admin-element-inner__input points-transactions__message fs-m"
                      rows="4"
                      placeholder="За что вы отправляете баллы"></textarea>
        </div>

        <span v-if="amount && amount > currentScore"
              class="send-points-form__warning">
            Недостаточно баллов. Доступно: {{ currentScore }}
        </span>

        <button class="primary-button points-transactions__submit"
                type="submit"
                :disabled="!canSubmit || isSending">
            {{ isSending ? 'Отправляем…' : 'Отправить' }}
        </button>
    </form>
    </div>
</template>

<script lang="ts">
import { computed, defineComponent, onUnmounted, ref } from 'vue';
import { watchDebounced } from '@vueuse/core';
import type { AxiosError } from 'axios';
import PointsInfoTable from '@/views/user/userPointsComponents/PointsInfoTable.vue';
import SearchList from '@/components/tools/common/SearchList.vue';
import Api from '@/utils/Api';
import type { IUserSearch } from '@/interfaces/IEntities';
import type { IPeerTransaction } from '@/interfaces/IPostFetch';
import { featureFlags } from '@/assets/static/featureFlags';
import { useUserData } from '@/stores/userData';
import { useUserScore } from '@/stores/userScoreData';
import { useToastCompose } from '@/composables/useToastСompose';
import { useToast } from 'primevue/usetoast';
import { handleApiError, handleApiResponse } from '@/utils/apiResponseCheck';

export default defineComponent({
    components: {
        PointsInfoTable,
        SearchList,
    },
    props: {
        pointsAboutImportant: {
            type: Boolean,
            default: () => false
        }
    },
    setup() {
        const abortController = new AbortController();
        const activeTab = ref<'history' | 'send'>('history');
        const searchQuery = ref('');
        const usersList = ref<IUserSearch[]>([]);
        const selectedUser = ref<IUserSearch | null>(null);
        const amount = ref<number | null>(null);
        const message = ref('');
        const isSearching = ref(false);
        const isSending = ref(false);
        const userData = useUserData();
        const userScore = useUserScore();
        const toast = useToastCompose(useToast());

        watchDebounced(searchQuery, async (query) => {
            usersList.value = [];
            if (!query) return;

            isSearching.value = true;
            try {
                const data = await Api.get(
                    `users/search/full_search_users_for_editor/${encodeURIComponent(query)}/10`,
                    null,
                    abortController.signal
                );
                const users = Array.isArray(data?.[0]?.content) ? data[0].content : [];
                usersList.value = users.filter((user: IUserSearch) =>
                    Number(user.id || user.user_id) !== userData.getMyId
                );
            } catch (error) {
                handleApiError(error as AxiosError, toast);
            } finally {
                isSearching.value = false;
            }
        }, { debounce: 500, maxWait: 1500 });

        const canSubmit = computed(() => {
            const points = Number(amount.value);
            return Boolean(
                selectedUser.value
                && message.value
                && Number.isInteger(points)
                && points > 0
                && points <= userScore.getCurrentScore
            );
        });

        const selectUser = (user: IUserSearch) => {
            selectedUser.value = user;
            usersList.value = [];
            searchQuery.value = '';
        };

        const clearSelectedUser = () => {
            selectedUser.value = null;
            searchQuery.value = '';
        };

        const sendPoints = async () => {
            if (!featureFlags.transactions || !canSubmit.value || !selectedUser.value) return;

            const transaction: IPeerTransaction = {
                user_from: userData.getMyId,
                user_to: selectedUser.value.id,
                message: message.value,
                how_match: Number(amount.value),
            };

            isSending.value = true;
            try {
                const response = await Api.post('peer/transaction', transaction);
                handleApiResponse(response, toast, 'trySupportError', 'pointsSendSuccess');

                const failed = !response || (
                    typeof response === 'object'
                    && 'status' in response
                    && ['warn', 'error'].includes(String(response.status))
                );
                if (failed) return;

                const history = await Api.get('peer/user_history');
                if (Array.isArray(history)) {
                    userScore.setStatistics(history);
                }
                selectedUser.value = null;
                amount.value = null;
                message.value = '';
                activeTab.value = 'history';
            } catch (error) {
                handleApiError(error as AxiosError, toast);
            } finally {
                isSending.value = false;
            }
        };

        onUnmounted(() => abortController.abort());

        return {
            activeTab,
            searchQuery,
            usersList,
            selectedUser,
            amount,
            message,
            isSearching,
            isSending,
            currentScore: computed(() => userScore.getCurrentScore),
            canSubmit,
            featureFlags,
            selectUser,
            clearSelectedUser,
            sendPoints,
        };
    },
})
</script>

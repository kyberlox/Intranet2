<template>
<div class="row">
    <div class="col-12 col-md-10">
        <div class="personal__user__section row"
             v-if="user">
            <div class="col-12 col-md-6">
                <div class="personal__user__photo">
                    <img v-if="user && user.photo_file_url"
                         :src="user.photo_file_url"
                         alt="Игорь"
                         @click="modalIsOpen = true" />
                    <img v-else
                         src="@/assets/imgs/plugs/userplug.jpg"
                         alt="Фото пользователя не найдено" />
                </div>
                <div class="personal__user__about">
                </div>
                <div class="personal__user__mess">
                    <a :href='"https://portal.emk.ru/company/personal/user/" + user.id + "/"'
                       target="_blank"
                       class="personal__user__mess__link primary-button">Профиль в Bitrix24</a>
                    <!-- <button v-if="user.id !== myId && featureFlags.pointsSystem"
                            class="personal__user__mess__link primary-button"
                            @click="isPointsModalOpen = true">Отправить баллы</button> -->
                </div>
            </div>

            <div class="col-12 col-md-6">
                <div class="personal__user__top">
                    <div class="grid__content-1">
                        <h3 class="personal__user__top__title">Контактная информация</h3>
                    </div>
                </div>
                <div class="personal__user__property">
                    <div v-for="(fields, column) in personalFields"
                         :key="column"
                         class="grid__content-1">
                        <div class="personal__user__property__items">
                            <template v-for="(field, key) in fields"
                                      :key="key">
                                <div v-if="field.values.length"
                                     :class="`personal__user__property__items__${key}`">
                                    <h3>{{ field.label }}</h3>
                                    <template v-for="(value, index) in field.values"
                                              :key="index">
                                        <span v-if="field.copyable"
                                              class="personal__user__property__items__copyable"
                                              role="button"
                                              tabindex="0"
                                              title="Скопировать"
                                              @click="copyField(value)"
                                              @keydown.enter.prevent="copyField(value)"
                                              @keydown.space.prevent="copyField(value)">{{ value }}</span>
                                        <span v-else>{{ value }}</span>
                                    </template>
                                </div>
                            </template>
                            <div v-if="column === 'contact'">
                                <h3 class="personal__user__top__title">Электронная визитная карточка</h3>
                                <RouterLink :to="{ name: 'vcard', params: { id: user.uuid } }"
                                            class="personal__user__vcard"
                                            :style="{ 'background-image': `url(${user.vcard_file_url})` }">
                                </RouterLink>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else
             class="contest__page__loader">
            <Loader />
        </div>
    </div>
    <ZoomModal :image="[user.photo_file_url ?? '@/assets/imgs/plugs/userplug.jpg']"
               v-if="modalIsOpen == true"
               @close="modalIsOpen = false" />
    <SendPoints v-if="isPointsModalOpen"
                @sendPoints="sendPoints"
                @close="isPointsModalOpen = false" />
</div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onUnmounted } from 'vue';
import Api from '@/utils/Api';
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import { watch } from 'vue';
import { useUserData } from '@/stores/userData';
import SendPoints from './userPointsComponents/SendPointsModalSlot.vue';
import { handleApiError, handleApiResponse } from '@/utils/apiResponseCheck';
import { useToastCompose } from '@/composables/useToastСompose';
import { useToast } from 'primevue/usetoast';
import type { IPointsForm } from '@/interfaces/IPutFetchData';
import { featureFlags } from '@/assets/static/featureFlags';
import Loader from '@/components/layout/Loader.vue';
import { useUserScore } from '@/stores/userScoreData';
import { createUniqueArr } from '@/utils/stringUtils';
import type { AxiosError } from 'axios';

export default defineComponent({
    props: {
        id: {
            type: String
        },
    },
    components: {
        ZoomModal,
        SendPoints,
        Loader
    },
    setup(props) {
        const abortController = new AbortController();
        const userData = useUserData();
        const user = ref();
        const modalIsOpen = ref(false);
        const isPointsModalOpen = ref(false);
        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);

        watch(() => props.id, async (newVal) => {
            if (newVal) {
                user.value = '';
                const res = await Api.get(`users/find_by/${newVal}`, null, abortController.signal)
                user.value = res;
                if (user.value && user.value.last_name && user.value.name && user.value.second_name) {
                    user.value.fio = user.value.last_name + " " + user.value.name + " " + user.value.second_name
                }
            }
        }, { immediate: true, deep: true })

        const copyField = async (value: string) => {
            value = String(value).trim();
            if (!value) return;

            try {
                await navigator.clipboard.writeText(value);
                toastInstance.add({ severity: 'success', summary: 'Скопировано', life: 2000 });
            } catch {
                toastInstance.add({ severity: 'error', summary: 'Не удалось скопировать', life: 3000 });
            }
        };

        const formatBirthday = (dateString: string): string => {
            if (!dateString) return '';

            const date = new Date(dateString);

            const russianMonths = [
                'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
            ];

            const day = date.getDate();
            const month = date.getMonth();

            return `${day} ${russianMonths[month]}`;
        }

        const senderId = computed(() => useUserData().getMyId);

        const sendPoints = async (comment: string, activityId: number) => {
            const sendingData: IPointsForm = {
                "uuid_from": senderId.value,
                "uuid_to": Number(props.id),
                "activities_id": activityId,
                "description": comment
            };
            try {
                const data = await Api.put('peer/send_points', sendingData)
                handleApiResponse(data, toast, 'trySupportError', 'pointsSendSuccess');
                try {
                    const data = await Api.get('peer/actions')
                    useUserScore().setActions(data)
                } catch (error) {
                    handleApiError(error as AxiosError, toast)
                }
            } catch (error) {
                handleApiError(error as AxiosError, toast)
            } finally {
                isPointsModalOpen.value = false
            }
        }

        const formatDate = (date: string) => {
            if (date.includes('T')) {
                const newDate = date.split('T')[0];
                const year = newDate.split('-')[0];
                const month = newDate.split('-')[1];
                const day = newDate.split('-')[2];
                return `${day}-${month}-${year}`
            }
            else return date.replaceAll('.', '-')
        }

        const personalFields = computed(() => ({
            personal: {
                'fio': {
                    label: 'ФИО',
                    values: [user.value?.fio].filter(Boolean),
                    copyable: true
                },
                'work-position': {
                    label: 'Должность',
                    values: [user.value?.indirect_data?.work_position].filter(Boolean),
                    copyable: true
                },
                'uf_usr_1696592324977': {
                    label: 'Дирекция',
                    values: user.value?.indirect_data?.uf_usr_1696592324977 ?? [],
                    copyable: true
                },
                'uf_usr_1705744824758': {
                    label: 'Отдел',
                    values: [...createUniqueArr(
                        user.value?.indirect_data?.uf_department ?? [],
                        user.value?.indirect_data?.uf_usr_1705744824758 ?? []
                    )],
                    copyable: true
                },
                'birthday': {
                    label: 'День рождения',
                    values: user.value?.personal_birthday ? [formatBirthday(user.value.personal_birthday)] : [],
                    copyable: true
                },
                'workplace': {
                    label: 'Местоположение',
                    values: [user.value?.personal_city].filter(Boolean),
                    copyable: true
                }
            },
            contact: {
                'email': {
                    label: 'Контактный e-mail',
                    values: [user.value?.email].filter(Boolean),
                    copyable: true
                },
                'office': {
                    label: 'Кабинет',
                    values: [user.value?.indirect_data?.uf_usr_1586854037086].filter(Boolean),
                    copyable: true
                },
                'inner-phone': {
                    label: 'Внутренний телефон',
                    values: [user.value?.uf_usr_1753418205828].filter(Boolean),
                    copyable: true
                },
                'work-phone': {
                    label: 'Рабочий телефон',
                    values: [user.value?.indirect_data?.work_phone].filter(Boolean),
                    copyable: true
                },
                'employment-date': {
                    label: 'Дата приема на работу',
                    values: user.value?.indirect_data?.date_of_employment
                        ? [formatDate(user.value.indirect_data.date_of_employment)] : [],
                    copyable: false
                }
            }
        }));

        onUnmounted(() => abortController.abort())

        return {
            user,
            modalIsOpen,
            isPointsModalOpen,
            featureFlags,
            myId: computed(() => userData.getMyId),
            sendPoints,
            personalFields,
            copyField
        }
    }
})
</script>

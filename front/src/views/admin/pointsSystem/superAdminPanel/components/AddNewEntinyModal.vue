<template>
<SlotModal>
    <div class="adminPointEditModal">
        <div v-if="currentEntity == 'activity'">
            <AdminEditInput @pick="(value: string) => newActivity.name = value"
                            :item="{ name: 'Название' }"
                            :placeholder="'Укажите название'" />
            <AdminEditInput @pick="(value: string) => newActivity.coast = Number(value)"
                            :item="{ name: 'Cтоимость' }"
                            :type="'number'"
                            :placeholder="'Укажите стоимость'" />

            <AdminEditSelect @pick="(value: string) => newActivity.need_valid = Boolean(value == 'true')"
                             :item="{ name: 'Доступно всем', values: ['true', 'false'] }" />

            <AdminEditInput v-if="!pickedUser && !newActivity.need_valid"
                            @pick="(value: string) => searchQuery = value"
                            :item="{ name: 'Куратор' }"
                            :placeholder="'Выберите сотрудника'" />

            <UsersSearchList v-if="usersList.length && !newActivity.need_valid"
                             :usersList="usersList"
                             @pickUser="(user: IUserSearch) => handleUserPick(user)" />

        </div>
        <div v-else
             class="adminPointEditModal">
            <AdminEditSelect v-if="currentEntity == 'curator'"
                             @pick="(value: string) => newActivity.activity_id = value"
                             :item="{ name: 'Активность', value: 0, values: usersActivities }" />

            <AdminEditInput v-if="!pickedUser"
                            @pick="(value: string) => searchQuery = value"
                            :item="{ name: currentEntity == 'curator' ? 'Куратор' : currentEntity == 'moder' ? 'Модератор' : 'Администратор' }"
                            :placeholder="'Выберите сотрудника'" />

            <UsersSearchList v-if="usersList.length"
                             :usersList="usersList"
                             @pickUser="(user: IUserSearch) => handleUserPick(user)" />
        </div>
        <button class="primary-button"
                @click="addActivity">Добавить</button>
    </div>
</SlotModal>
</template>

<script lang="ts">
import { defineComponent, ref, watch, computed } from 'vue';
import SlotModal from '@/components/tools/modal/SlotModal.vue';
import AdminEditInput from '@/views/admin/components/inputFields/AdminEditInput.vue';
import AdminEditSelect from '@/views/admin/components/inputFields/AdminEditSelect.vue';
import Api from '@/utils/Api';
import { handleApiError } from '@/utils/ApiResponseCheck';
import { useToastCompose } from '@/composables/useToastСompose';
import { useToast } from 'primevue/usetoast';
import UsersSearchList from '@/components/tools/common/UsersSearchList.vue';
import type { IUserSearch } from '@/interfaces/IEntities';
import { watchDebounced } from '@vueuse/core';
import { usePointsData } from '@/stores/PointsData';

import type { INewActivityData } from '@/interfaces/IPutFetchData';

export default defineComponent({
    components: {
        SlotModal,
        AdminEditInput,
        AdminEditSelect,
        UsersSearchList
    },
    props: {
        currentEntity: {
            type: String
        }
    },
    emits: ['addNew'],
    setup(props, { emit }) {
        const newActivity = ref<INewActivityData>({});
        const usersActivities = computed(() => usePointsData().getActivities);

        const searchQuery = ref();
        const usersList = ref<IUserSearch[]>([]);
        const pickedUser = ref<IUserSearch | null>(null);

        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);

        const handleUserPick = (user: IUserSearch) => {
            pickedUser.value = user;
            usersList.value = usersList.value.filter((e) => e.id == user.id);
            newActivity.value!.uuid = user.id;
        }

        watchDebounced((searchQuery), () => {
            if (!searchQuery.value) return;
            Api.get(`users/search/full_search_users/${searchQuery.value}`)
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .then((data) => {
                    usersList.value = data[0].content;
                });
        }, { debounce: 500, maxWait: 1500 })

        watch((props), () => {
            if (props.currentEntity) {
                usersList.value.length = 0
                searchQuery.value = ''
                pickedUser.value = null
                newActivity.value = {}
            }
        })

        const addActivity = () => {
            emit('addNew', newActivity.value);
        }

        return {
            searchQuery,
            usersList,
            newActivity,
            pickedUser,
            usersActivities,
            addActivity,
            handleUserPick
        }
    }
})
</script>


<style>
.adminPointEditModal {
    padding: 20px;
    /* width: 500px; */
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>
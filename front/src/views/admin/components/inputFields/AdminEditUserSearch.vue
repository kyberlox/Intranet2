<template>
<AdminEditInput v-if="!pickedUser"
                @pick="(value: string) => searchQuery = value"
                :item="{ name: 'Сотрудник' }"
                :placeholder="'Выберите сотрудника'" />

<UsersSearchList v-if="usersList.length"
                 :usersList="usersList"
                 @pickUser="(user: IUserSearch) => handleUserPick(user)" />
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import UsersSearchList from '@/components/tools/common/UsersSearchList.vue';
import AdminEditInput from './AdminEditInput.vue';
import type { IUserSearch } from '@/interfaces/IEntities';
import { watchDebounced } from '@vueuse/core';
import Api from '@/utils/Api';
import { handleApiError } from '@/utils/ApiResponseCheck';
import { useToastCompose } from '@/composables/useToastСompose';
import { useToast } from 'primevue/usetoast';

export default defineComponent({
    components: {
        UsersSearchList,
        AdminEditInput
    },
    emits: ['userPicked'],
    setup(_, { emit }) {
        const pickedUser = ref();
        const usersList = ref([]);
        const searchQuery = ref<string>();

        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);

        const handleUserPick = (user: IUserSearch) => {
            pickedUser.value = user;
            usersList.value = usersList.value.filter((e: IUserSearch) => e.id == user.id);
            emit('userPicked', user.id)
        }

        watchDebounced((searchQuery), () => {
            if (!searchQuery.value) return;
            Api.get(`users/search/full_search_users_for_editor/${searchQuery.value}/5`)
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .then((data) => {
                    usersList.value = data[0].content;
                });
        }, { debounce: 500, maxWait: 1500 })

        return {
            pickedUser,
            usersList,
            searchQuery,
            handleUserPick
        }
    }
})
</script>
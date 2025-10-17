<template>
<div class="admin-element__reportage-group__add-button__wrapper admin-element__add-user__button__group">
    <p class="admin-element-inner__field-title fs-l">заполнить данными о сотруднике</p>
    <div @click="showSearchModal = true"
         class="admin-element__reportage-group__add-button primary-button">
        <PlusIcon />
    </div>
</div>
<SlotModal v-if="showSearchModal"
           @close="showSearchModal = false">
    <AdminEditInput v-if="!pickedUser"
                    @pick="(value: string) => (searchQuery = value)"
                    :item="{ name: 'Сотрудник' }"
                    :placeholder="'Выберите сотрудника'" />

    <UsersSearchList v-if="usersList.length"
                     :usersList="usersList"
                     @pickUser="(user: IUserSearch) => handleUserPick(user)" />
</SlotModal>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import UsersSearchList from '@/components/tools/common/UsersSearchList.vue'
import AdminEditInput from './AdminEditInput.vue'
import type { IUserSearch } from '@/interfaces/IEntities'
import { watchDebounced } from '@vueuse/core'
import Api from '@/utils/Api'
import { handleApiError } from '@/utils/ApiResponseCheck'
import { useToastCompose } from '@/composables/useToastСompose'
import { useToast } from 'primevue/usetoast'
import SlotModal from '@/components/tools/modal/SlotModal.vue'
import PlusIcon from '@/assets/icons/admin/PlusIcon.svg?component'

export default defineComponent({
    components: {
        UsersSearchList,
        AdminEditInput,
        SlotModal,
        PlusIcon,
    },
    props: {
        type: {
            type: String
        },
    },
    name: 'adminEditUserSearch',
    emits: ['usersPicked', 'userPicked'],
    setup(props, { emit }) {
        const pickedUser = ref()
        const usersList = ref([])
        const searchQuery = ref<string>()

        const toastInstance = useToast()
        const toast = useToastCompose(toastInstance)

        const showSearchModal = ref(false)

        const handleUserPick = (user: IUserSearch) => {
            pickedUser.value = user;
            usersList.value = usersList.value.filter((e: IUserSearch) => e.id == user.id);
            emit((props.type == 'search_by_uuids' ? 'usersPicked' : 'userPicked'), user.id);
            pickedUser.value = false;
            showSearchModal.value = false;
            usersList.value.length = 0;
        }

        watchDebounced(
            searchQuery,
            () => {
                if (!searchQuery.value) return
                Api.get(`users/search/full_search_users_for_editor/${searchQuery.value}/5`)
                    .catch((error) => {
                        if (error.response?.status == 500) {
                            handleApiError(error, toast)
                        }
                    })
                    .then((data) => {
                        usersList.value = data[0].content
                    })
            },
            { debounce: 500, maxWait: 1500 },
        )

        return {
            pickedUser,
            usersList,
            searchQuery,
            showSearchModal,
            handleUserPick,
        }
    },
})
</script>
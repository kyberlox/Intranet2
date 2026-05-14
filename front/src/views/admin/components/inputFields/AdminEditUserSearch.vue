<template>
<div v-if="inPost"
     class="admin-element__reportage-group__add-button__wrapper admin-element__add-user__button__group">
    <p class="admin-element-inner__field-title fs-l">заполнить данными о сотруднике</p>
    <div @click="showSearchModal = true"
         class="admin-element__reportage-group__add-button primary-button">
        <PlusIcon />
    </div>
</div>
<div v-else>
    <p v-if="title"
       class="admin-element-inner__field-title fs-l">
        {{ title }}
    </p>
    <div class="primary-button"
         @click="showSearchModal = true">Добавить</div>
</div>
<SearchList v-if="users.length && (field == 'implementer' || field == 'integrator')"
            :searchList="users"
            :needDeleteButton="needDeleteButton"
            @remove="(user: IUserSearch) => handleUserPick(user, 'remove')"
            @pick="(user: IUserSearch) => handleUserPick(user)" />
<SlotModal v-if="showSearchModal"
           @close="showSearchModal = false">
    <AdminEditInput v-if="!pickedUser"
                    @pick="(value: string) => (searchQuery = value)"
                    :item="{ name: 'Сотрудник' }"
                    :placeholder="'Выберите сотрудника'" />

    <SearchList v-if="usersList.length"
                :searchList="usersList"
                :needDeleteButton="needDeleteButton"
                @remove="(user: IUserSearch) => handleUserPick(user, 'remove')"
                @pick="(user: IUserSearch) => handleUserPick(user)" />
</SlotModal>
</template>

<script lang="ts">
import { defineComponent, ref, type PropType } from 'vue'
import SearchList, { type IUserList } from '@/components/tools/common/SearchList.vue'
import AdminEditInput from './AdminEditInput.vue'
import type { IAdminListItem, IUserSearch } from '@/interfaces/IEntities'
import { watchDebounced } from '@vueuse/core'
import Api from '@/utils/Api'
import { handleApiError } from '@/utils/apiResponseCheck'
import { useToastCompose } from '@/composables/useToastСompose'
import { useToast } from 'primevue/usetoast'
import SlotModal from '@/components/tools/modal/SlotModal.vue'
import PlusIcon from '@/assets/icons/admin/PlusIcon.svg?component'

export default defineComponent({
    components: {
        SearchList,
        AdminEditInput,
        SlotModal,
        PlusIcon,
    },
    props: {
        type: {
            type: String,
        },
        inPost: {
            type: Boolean,
            deafault: true,
        },
        title: {
            type: String,
        },
        field: {
            type: String,
        },
        users: {
            type: Array<IUserList>,
            default: () => [],
        },
        needDeleteButton: {
            type: Boolean,
        },
    },
    name: 'adminEditUserSearch',
    emits: ['handleUserPick', 'handleUsersPick'],
    setup(props, { emit }) {
        const pickedUser = ref()
        const usersList = ref([])
        const searchQuery = ref<string>()

        const toastInstance = useToast()
        const toast = useToastCompose(toastInstance)

        const showSearchModal = ref(false)

        const handleUserPick = (user: IUserSearch, type: string = '') => {
            pickedUser.value = user
            usersList.value = usersList.value.filter((e: IUserSearch) => e.id == user.id)
            emit(
                props.type == 'search_by_uuids' ? 'handleUsersPick' : 'handleUserPick',
                type == 'remove' ? null : user.id ? user.id : user.user_id,
                (props.field == 'implementer' || props.field == 'integrator') ? props.field : 'base',
            )
            pickedUser.value = false
            showSearchModal.value = false
            usersList.value.length = 0
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

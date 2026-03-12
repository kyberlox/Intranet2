<template>
<AdminEditInput :item="{ name: 'ID предприятия', disabled: 'true', value: pickedId || idValue }"
                :placeholder="`Нажмите 'добавить' и выберите предприятие, чтобы сохранить его id `" />
<div class="primary-button"
     @click="showSearchModal = true">
    Добавить
</div>
<SlotModal v-if="showSearchModal"
           @close="showSearchModal = false">
    <AdminEditInput v-if="!pickedId"
                    @pick="(value: string) => (searchQuery = value)"
                    :item="{ name: 'Поиск по структуре' }"
                    :placeholder="'Выберите отдел, его данные сохранятся'" />

    <AdminUsersList :users="departmentList"
                    :type="'departments'"
                    @pickUser="(user: IUserSearch) => handleDepIdPick(user)" />
</SlotModal>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import AdminEditInput from './AdminEditInput.vue'
import type { IUserSearch } from '@/interfaces/IEntities'
import { watchDebounced } from '@vueuse/core'
import Api from '@/utils/Api'
import { handleApiError } from '@/utils/apiResponseCheck'
import { useToastCompose } from '@/composables/useToastСompose'
import { useToast } from 'primevue/usetoast'
import SlotModal from '@/components/tools/modal/SlotModal.vue'
import AdminUsersList from './AdminUsersList.vue'

export interface IAreaDepartment {
    id: number,
    name: string
}

export default defineComponent({
    components: {
        AdminEditInput,
        SlotModal,
        AdminUsersList
    },
    props: {
        type: {
            type: String
        },
        idValue: {
            type: Number
        }
    },
    name: 'adminEditUserSearch',
    emits: ['handleDepartmentPick'],
    setup(props, { emit }) {
        const pickedId = ref()
        const departmentList = ref<IAreaDepartment[]>([])
        const searchQuery = ref<string>()

        const toastInstance = useToast()
        const toast = useToastCompose(toastInstance)

        const showSearchModal = ref(false)

        const handleDepIdPick = (dep: IAreaDepartment) => {
            pickedId.value = dep.id;
            emit('handleDepartmentPick', dep.id);
            showSearchModal.value = false;
        }

        watchDebounced(
            searchQuery,
            () => {
                if (!searchQuery.value) return
                getDepStructureByName(searchQuery.value)
            },
            { debounce: 500, maxWait: 1500 },
        )

        const getDepStructureByName = (word: string) => {
            Api.get(`fields_visions/get_dep_structure_by_name/${word}`)
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .then((data) => {
                    departmentList.value = data;
                })
        }

        return {
            searchQuery,
            showSearchModal,
            pickedId,
            departmentList,
            handleDepIdPick
        }
    },
})
</script>
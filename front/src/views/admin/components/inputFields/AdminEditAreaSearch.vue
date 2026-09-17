<template>
<AdminEditInput v-if="!multiple" :item="{ name: 'ID предприятия', disabled: 'true', value: pickedId || idValue || '' }"
                :placeholder="`Нажмите 'добавить' и выберите предприятие, чтобы сохранить его id `" />
<div class="primary-button"
     @click="showSearchModal = true">
    Добавить
</div>
<SlotModal v-if="showSearchModal"
           @close="showSearchModal = false">
    <AdminEditInput v-if="multiple || !pickedId"
                    @pick="(value: string) => (searchQuery = value)"
                    :item="{ name: 'Поиск по структуре' }"
                    :placeholder="'Выберите отдел, его данные сохранятся'" />

    <SearchList :searchList="departmentList"
                :type="'departments'"
                @pick="(department: IAreaDepartment) => handleDepIdPick(department)" />
</SlotModal>
</template>

<script lang="ts">
import { defineComponent, ref, onUnmounted } from 'vue'
import AdminEditInput from './AdminEditInput.vue'
import { watchDebounced } from '@vueuse/core'
import Api from '@/utils/Api'
import { handleApiError } from '@/utils/apiResponseCheck'
import { useToastCompose } from '@/composables/useToastСompose'
import { useToast } from 'primevue/usetoast'
import SlotModal from '@/components/tools/modal/SlotModal.vue'
import SearchList from '@/components/tools/common/SearchList.vue'
import type { AxiosError } from 'axios'

export interface IAreaDepartment {
    id: number,
    name: string
}

export default defineComponent({
    components: {
        AdminEditInput,
        SlotModal,
        SearchList
    },
    props: {
        multiple: {
            type: Boolean,
            default: false
        },
        type: {
            type: String
        },
        idValue: {
            type: Number
        }
    },
    name: 'adminEditAreaSearch',
    emits: ['handleDepartmentPick'],
    setup(props, { emit }) {
        const abortController = new AbortController();
        const pickedId = ref('')
        const departmentList = ref<IAreaDepartment[]>([])
        const searchQuery = ref<string>()

        const toastInstance = useToast()
        const toast = useToastCompose(toastInstance)

        const showSearchModal = ref(false)

        const handleDepIdPick = (dep: IAreaDepartment) => {
            pickedId.value = String(dep.id);
            emit('handleDepartmentPick', dep.id, dep.name);
            showSearchModal.value = false;
            if (props.multiple) {
                searchQuery.value = '';
                departmentList.value = [];
            }
        }

        watchDebounced(
            searchQuery,
            () => {
                if (!searchQuery.value) return
                getDepStructureByName(searchQuery.value)
            },
            { debounce: 500, maxWait: 1500 },
        )

        const getDepStructureByName = async (word: string) => {
            try {
                const data = await Api.get(`fields_visions/get_dep_structure_by_name/${word}`, null, abortController.signal)
                departmentList.value = data;
            }
            catch (error: unknown) {
                if ((error as AxiosError).response?.status == 500) {
                    handleApiError(error as AxiosError, toast)
                }
            }
        }

        onUnmounted(() => abortController.abort())

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

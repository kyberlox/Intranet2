<template>
<div class="admin-panel">
    <div class="admin-panel__sidebar">
        <div class="visibility-editor__wrapper">
            <AdminSidebar :needDefaultNav="false">
                <div class="admin-panel__header">
                    <h3 class="admin-panel__title">
                        Настройка прав пользователей
                    </h3>
                </div>
                <ul v-if="newSections.length"
                    class="admin-panel__nav-list">
                    <li v-for="(section, index) in newSections"
                        :key="'section' + index"
                        class="admin-panel__nav-item"
                        @click="activeSection = section">
                        <div class="admin-panel__nav-link"
                             :class="{ 'admin-panel__nav-link--active': (activeSection && 'name' in activeSection && section.name == activeSection.name) }">
                            <div class="admin-panel__nav-icon">
                                <NavArrow />
                            </div>
                            <span class="admin-panel__nav-text">
                                {{ section.name }}
                            </span>
                        </div>
                    </li>
                </ul>
            </AdminSidebar>
        </div>
    </div>
    <div v-if="activeSection && !isLoading"
         class="admin-panel__content admin-panel__content__add-user-btn">
        <AdminEditUserSearch @handleUserPick="addRootToUser" />
        <SearchList :searchList="activeSectionEditors"
                    :needDeleteButton="true"
                    @remove="(id: number) => removeUsersRoot(id)" />
    </div>
    <div v-else-if="!activeSection && isLoading"
         class="admin-panel__content admin-panel__content__add-user-btn contest__page__loader">
        <Loader />
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, computed, ref, watch } from 'vue';
import { useAdminData } from '@/stores/adminData';
import AdminSidebar from '../components/AdminSidebar.vue';
import NavArrow from '@/assets/icons/admin/NavArrow.svg?component'
import Api from '@/utils/Api';
import AdminEditUserSearch from '../components/inputFields/AdminEditUserSearch.vue';
import SearchList, { type IUserList } from '@/components/tools/common/SearchList.vue';
import Loader from '@/components/layout/Loader.vue';
import { useUserData } from '@/stores/userData';

export default defineComponent({
    name: 'rootsEditPanel',
    components: {
        AdminSidebar,
        NavArrow,
        AdminEditUserSearch,
        SearchList,
        Loader
    },
    setup() {
        const sections = computed(() => useAdminData().getSections)
        const activeSection = ref();
        const activeSectionEditors = ref<IUserList[]>([]);
        const isLoading = ref(false);
        const gptRoot = computed(() => useUserData().getUserRoots.GPT_gen_access || useUserData().getUserRoots.EditorAdmin);
        const newSections = ref<{ id: string | number; name: string; }[]>([]);

        watch([sections, gptRoot], ([sectionsVal, gptVal]) => {
            if (gptVal && sectionsVal.length) {
                newSections.value = [...sectionsVal];
                if (!newSections.value.find((e) => e.id === 'gpt')) {
                    newSections.value.push({ id: 'gpt', name: 'Доступ к gpt' });
                }
            } else {
                newSections.value = [...sectionsVal];
            }
        }, { immediate: true, deep: true })

        watch(activeSection, () => {
            if (!activeSection.value) return
            editorsInit()
        }, { immediate: true })

        const editorsInit = async () => {
            isLoading.value = true;
            if (activeSection.value.id == 'gpt') {
                try {
                    const data = await Api.get('roots/get_gpt_gen_licenses')
                    activeSectionEditors.value = data
                } finally {
                    isLoading.value = false
                }
            }
            else
                try {
                    const data = await Api.get(`roots/get_editors_list/${activeSection.value.id}`)
                    activeSectionEditors.value = Array.isArray(data) ? data : []
                } finally {
                    isLoading.value = false
                }
        }

        const addRootToUser = async (id: number) => {
            try {
                if (activeSection.value.id == 'gpt') {
                    await Api.put('roots/give_gpt_gen_license', [id])
                }
                else {
                    await Api.put(`roots/create_editor_moder/${id}/${activeSection.value.id}`)
                }
                editorsInit()
            } catch (error) {
                console.error(error)
            } finally {
                isLoading.value = false
            }
        }

        const removeUsersRoot = async (id: number) => {
            try {
                if (activeSection.value.id == 'gpt') {
                    await Api.delete(`/roots/stop_gpt_gen_license/${id}`)
                }
                else {
                    await Api.delete(`roots/delete_editor_moder/${id}/${activeSection.value.id}`)
                }
                editorsInit()
            } catch (error) {
                console.error(error)
            }
        }

        return {
            newSections,
            activeSection,
            activeSectionEditors,
            isLoading,
            addRootToUser,
            removeUsersRoot
        }
    }
})
</script>
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
        <AdminUsersList :users="activeSectionEditors"
                        @removeUser="(id: number) => removeUsersRoot(id)" />
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
import AdminUsersList, { type IUserList } from '../components/inputFields/AdminUsersList.vue';
import Loader from '@/components/layout/Loader.vue';
import { useUserData } from '@/stores/userData';

export default defineComponent({
    name: 'rootsEditPanel',
    components: {
        AdminSidebar,
        NavArrow,
        AdminEditUserSearch,
        AdminUsersList,
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

        const editorsInit = () => {
            isLoading.value = true;
            if (activeSection.value.id == 'gpt') {
                Api.get('roots/get_gpt_gen_licenses')
                    .then((data) => activeSectionEditors.value = data)
                    .finally(() => isLoading.value = false)
            }
            else
                Api.get(`roots/get_editors_list/${activeSection.value.id}`)
                    .then((data) => Array.isArray(data) ? activeSectionEditors.value = data : activeSectionEditors.value = [])
                    .finally(() => isLoading.value = false)
        }

        const addRootToUser = (id: number) => {
            if (activeSection.value.id == 'gpt') {
                Api.put('roots/give_gpt_gen_license', [id])
                    .then(() => editorsInit())
                    .finally(() => isLoading.value = false)
            }
            else
                Api.put(`roots/create_editor_moder/${id}/${activeSection.value.id}`)
                    .then(() => editorsInit())
        }

        const removeUsersRoot = (id: number) => {
            if (activeSection.value.id == 'gpt') {
                Api.delete(`/roots/stop_gpt_gen_license/${id}`)
                    .finally(() => editorsInit())
            }
            else
                Api.delete(`roots/delete_editor_moder/${id}/${activeSection.value.id}`)
                    .then(() => editorsInit())
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
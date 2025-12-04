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
                <ul v-if="sections.length"
                    class="admin-panel__nav-list">
                    <li v-for="(section, index) in sections"
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
        <AdminEditUserSearch @userPicked="addRootToUser" />
        <AdminUsersList :users="activeSectionEditors"
                        @removeUser="(id: number) => removeUsersRoot(id)" />
    </div>
    <div class="admin-panel__content admin-panel__content__add-user-btn"
         v-else>
        <Loader class="contest__page__loader" />
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
import AdminUsersList from '../components/inputFields/AdminUsersList.vue';
import Loader from '@/components/layout/Loader.vue';

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
        const activeSectionEditors = ref([]);
        const isLoading = ref(false);

        watch((activeSection), () => {
            if (!activeSection.value) return
            editorsInit()
        }, { immediate: true, deep: true })

        const editorsInit = () => {
            isLoading.value = true;
            Api.get(`roots/get_editors_list/${activeSection.value.id}`)
                .then((data) => activeSectionEditors.value = data)
                .finally(() => isLoading.value = false)
        }

        const addRootToUser = (id: number) => {
            Api.put(`roots/create_editor_moder/${id}/${activeSection.value.id}`)
                .then(() => editorsInit())
        }

        const removeUsersRoot = (id: number) => {
            Api.delete(`roots/delete_editor_moder/${id}/${activeSection.value.id}`)
                .then(() => editorsInit())
        }

        return {
            sections,
            activeSection,
            activeSectionEditors,
            isLoading,
            addRootToUser,
            removeUsersRoot
        }
    }
})
</script>
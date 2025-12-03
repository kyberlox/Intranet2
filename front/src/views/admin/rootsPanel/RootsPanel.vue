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
    <div v-if="activeSection"
         class="admin-panel__content admin-panel__content__add-user-btn">
        <AdminEditUserSearch @userPicked="addRootToUser" />
        <AdminUsersList :users="activeSectionEditors" />
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

export default defineComponent({
    name: 'rootsEditPanel',
    components: {
        AdminSidebar,
        NavArrow,
        AdminEditUserSearch,
        AdminUsersList
    },
    setup() {
        const sections = computed(() => useAdminData().getSections)
        const activeSection = ref();
        const activeSectionEditors = ref([]);

        watch((activeSection), () => {
            if (!activeSection.value) return
            Api.get(`roots/get_editors_list/${activeSection.value.id}`)
                .then((data) => activeSectionEditors.value = data)
        }, { immediate: true, deep: true })

        const addRootToUser = (id: number) => {
            Api.put(`roots/create_editor_moder/${id}/${activeSection.value.id}`)
                .then((data) => console.log(data))
        }

        return {
            sections,
            activeSection,
            activeSectionEditors,
            addRootToUser
        }
    }
})
</script>
<template>
<div class="visibility-editor__title page__title mt20">
    Настройка прав пользователей
</div>
<div class="visibility-editor__wrapper">
    <AdminSidebar :needDefaultNav="false">
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
</template>

<script lang="ts">
import { defineComponent, computed, ref } from 'vue';
import { useAdminData } from '@/stores/adminData';
import AdminSidebar from '../components/AdminSidebar.vue';
import NavArrow from '@/assets/icons/admin/NavArrow.svg?component'

export default defineComponent({
    name: 'rootsEditPanel',
    components: {
        AdminSidebar,
        NavArrow
    },
    setup() {
        const sections = computed(() => useAdminData().getSections)
        const activeSection = ref();

        return {
            sections,
            activeSection
        }
    }
})
</script>
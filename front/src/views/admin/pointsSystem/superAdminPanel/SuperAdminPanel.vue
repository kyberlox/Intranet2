<template>
    <div class="points-admin-panel__wrapper">
        <div class="points-admin-panel">
            <div class="points-admin-panel__navigation__wrapper">
                <nav class="points-admin-panel__navigation"
                     :class="{ 'points-admin-panel__navigation--active': tab.id == activeTab }"
                     v-for="tab in navTabs"
                     :key="tab.id"
                     @click="changeTab(tab.id)">
                    {{ tab.name }}
                </nav>
            </div>
            <div v-if="activeTab"
                 class="points-admin-panel__content">
                <EditTable :activeId="activeTab" />
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

import EditTable from './components/PointsEditTable.vue';
export default defineComponent({
    components: {
        EditTable
    },
    setup() {
        const activeTab = ref();
        const navTabs = [
            { id: 1, name: 'Активности' },
            { id: 2, name: 'Кураторы' },
            { id: 3, name: 'Модераторы' },
            { id: 4, name: 'Администраторы' }
        ];

        const changeTab = (id: number) => {
            activeTab.value = id;
        }

        return {
            activeTab,
            navTabs,
            changeTab
        }
    }
})
</script>
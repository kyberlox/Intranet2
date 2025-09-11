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

import EditTable from './components/EditTable.vue';
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

<style>
.points-admin-panel__navigation__wrapper {
    display: flex;
    flex-direction: row;
    gap: 8px;
    padding: 12px;
    border-bottom: 1px solid #eef2f6;
    background: #fafbfd;
    align-items: center;
    flex-wrap: wrap;
}

.points-admin-panel__navigation {
    padding: 8px 14px;
    border-radius: 10px;
    color: #5a6b82;
    background: transparent;
    font-weight: 600;
    line-height: 1;
    letter-spacing: 0.2px;
    cursor: pointer;
    user-select: none;
    transition:
        color 0.2s ease,
        background-color 0.2s ease,
        box-shadow 0.2s ease,
        transform 0.02s ease;
    border: 1px solid transparent;

    &--active {
        transform: translateY(0.5px);
    }
}

.points-admin-panel__navigation:hover {
    background: #f1f5f9;
    color: var(--emk-brand-color);
}

.points-admin-panel__navigation:active {
    transform: translateY(0.5px);
}

.points-admin-panel__navigation--active {
    border: 1px solid var(--emk-brand-color);
}

.points-admin-panel {
    display: flex;
    flex-direction: column;
}
</style>
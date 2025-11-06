<template>
    <nav class="admin-panel__nav">
        <h6 class="admin-panel__nav-title mt20">Активности</h6>
        <ul class="admin-panel__nav-list">
            <li v-for="(activity, index) in moderatorsActivities"
                :key="'section' + index"
                class="admin-panel__nav-item"
                @click="$emit('areaClicked', activity.id)">
                <div class="admin-panel__nav-link"
                     :class="{ 'admin-panel__nav-link--active': activeId == activity.id }">
                    <div class="admin-panel__nav-icon">
                        <NavArrow />
                    </div>
                    <span class="admin-panel__nav-text">{{ activity.name }}</span>
                </div>
            </li>
        </ul>
    </nav>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import type { IActivitiesList } from '@/interfaces/IEntities';
import NavArrow from '@/assets/icons/admin/NavArrow.svg?component'
export default defineComponent({
    name: 'ModeratorSidebarSlot',
    props: {
        moderatorsActivities: {
            type: Array as PropType<IActivitiesList[]>

        },
        activeId: {
            type: Number
        }
    },
    components: {
        NavArrow
    },
    setup() {

        return {

        }
    }
})
</script>
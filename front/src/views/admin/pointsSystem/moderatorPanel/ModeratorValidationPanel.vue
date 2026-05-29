<template>
<div class="moderator-panel">
    <AdminSidebar :needDefaultNav="false">
        <ModeratorSidebarSlot @areaClicked="changeActive"
                              :activeId="activeId"
                              :moderatorsActivities="activitiesToConfirm" />
    </AdminSidebar>

    <PointsHistoryActionTable v-if="activeId"
                              @moderate="moderate"
                              :activitiesInTable="activitiesInTable" />
</div>
</template>

<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import Api from '@/utils/Api';
import { usePointsData } from '@/stores/pointsData';
import AdminSidebar from '@/views/admin/components/AdminSidebar.vue';
import { dateConvert } from '@/utils/dateConvert';
import ModeratorSidebarSlot from './ModeratorSidebarSlot.vue';
import PointsHistoryActionTable from '../PointsHistoryActionTable.vue';
import type { IActivityToConfirm } from '@/interfaces/IEntities';

export default defineComponent({
    name: 'moderatorValidationPanel',
    components: {
        PointsHistoryActionTable,
        AdminSidebar,
        ModeratorSidebarSlot
    },
    setup() {
        const activeId = ref<number>();
        const activitiesToConfirm = computed(() => usePointsData().getActivitiesToConfirm);
        const activitiesInTable = ref<IActivityToConfirm[]>();

        const changeActive = (id: number) => {
            activeId.value = id;
        }

        const tableInit = async () => {
            try {
                const data = await Api.get(`peer/points_to_confirm/${activeId.value}`)
                activitiesInTable.value = data
            } catch (error) {
                console.error(error)
            }
        }

        watch((activeId), () => {
            if (!activeId.value) return
            tableInit();
        }, { immediate: true, deep: true });

        const moderate = async (type: 'accept' | 'cancel', rowId: number, uuidTo: number) => {
            try {
                await Api.post(`/peer/${type == 'accept' ? 'do_valid' : 'do_not_valid'}/${rowId}${type == 'accept' ? '/' + uuidTo : ''}`)
                tableInit()
            } catch (error) {
                console.error(error)
            }
        }

        return {
            activitiesToConfirm,
            activitiesInTable,
            activeId,
            dateConvert,
            changeActive,
            moderate
        }
    }
})
</script>

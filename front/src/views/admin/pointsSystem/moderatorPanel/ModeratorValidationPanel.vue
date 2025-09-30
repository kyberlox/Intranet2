<template>
<div class="moderator-panel">
    <AdminSidebar :needDefaultNav="false">
        <ModeratorSidebarSlot @areaClicked="changeActive"
                              :activeId="activeId"
                              :moderatorsActivities="activitiesToConfirm" />
    </AdminSidebar>

    <PointsHistoryActionTable v-if="activeId"
                              :onlyHistory="true"
                              :activitiesInTable="activitiesInTable" />
</div>
</template>

<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import Api from '@/utils/Api';
import { usePointsData } from '@/stores/PointsData';
import AdminSidebar from '@/views/admin/components/elementsListLayout/AdminSidebar.vue';
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

        const tableInit = () => {
            Api.get(`peer/points_to_confirm/${activeId.value}`)
                .then((data) => {
                    activitiesInTable.value = data
                })
        }

        watch((activeId), () => {
            if (!activeId.value) return
            tableInit();
        }, { immediate: true, deep: true });

        const moderate = (type: 'accept' | 'cancel', rowId: number, uuidTo: number) => {
            Api.post(`/api/peer/${type == 'accept' ? 'do_valid' : 'do_not_valid'}`, { action_id: rowId, uuid_to: uuidTo })
                .then((data) => console.log(data))
                .finally(() => tableInit())
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
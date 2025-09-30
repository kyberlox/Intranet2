<template>
<PointsHistoryActionTable :needCheckButton="false"
                          :activitiesInTable="activitiesInTable"
                          @moderate="cancelPoints" />
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import PointsHistoryActionTable from '../PointsHistoryActionTable.vue';
import type { IActivityToConfirm } from '@/interfaces/IEntities';
export default defineComponent({
    components: {
        PointsHistoryActionTable
    },
    setup() {
        const activitiesInTable = ref<IActivityToConfirm[]>([]);

        const cancelPoints = () => {
            console.log('галя отмена');
        }

        return {
            activitiesInTable,
            cancelPoints
        }
    }
})
</script>

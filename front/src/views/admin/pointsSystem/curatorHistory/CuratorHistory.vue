<template>
<PointsHistoryActionTable :needCheckButton="false"
                          :onlyHistory="true"
                          :activitiesInTable="activitiesInTable"
                          @moderate="moderate" />
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import PointsHistoryActionTable from '../PointsHistoryActionTable.vue';
import type { ICuratorActivityHistory } from '@/interfaces/IEntities';
import Api from '@/utils/Api';
export default defineComponent({
    components: {
        PointsHistoryActionTable
    },
    setup() {
        const activitiesInTable = ref<ICuratorActivityHistory[]>([]);

        onMounted(() => {
            tableInit();
        })

        const moderate = (a: string, actionId: number, uuid: number, valid?: number) => {
            Api.post(`peer/remove_user_points/${uuid}/${actionId}/${valid}`)
                .finally(() => tableInit())
        }

        const tableInit = () => {
            Api.get('peer/get_curators_history')
                .then((data: ICuratorActivityHistory[]) => activitiesInTable.value = data)
        }

        return {
            activitiesInTable,
            moderate
        }
    }
})
</script>

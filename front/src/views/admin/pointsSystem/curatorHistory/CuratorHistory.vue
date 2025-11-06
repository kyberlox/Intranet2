<template>
<PointsHistoryActionTable :needCheckButton="false"
                          :onlyHistory="true"
                          :activitiesInTable="activitiesInTable" />
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
            Api.get('peer/get_curators_history')
                .then((data: ICuratorActivityHistory[]) => activitiesInTable.value = data)
        })

        return {
            activitiesInTable,
        }
    }
})
</script>

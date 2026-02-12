<template><!-- <div v-if="needFilter">
    <button @click="showFilter = !showFilter"
            class="btn dropdown-toggle tagDateNavBar__dropdown-toggle">
        Активность
    </button>
    <CustomFilter v-if="showFilter"
                  :params="filterYears"
                  :buttonText="currentYear ?? 'Год'"
                  @pickFilter="(year: string) => currentYear = year" />
</div> -->
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
import CustomFilter from '@/components/tools/common/CustomFilter.vue';

export default defineComponent({
    components: {
        PointsHistoryActionTable,
        CustomFilter
    },
    props: {
        needFilter: {
            type: Boolean,
            default: () => false
        }
    },
    setup() {
        const activitiesInTable = ref<ICuratorActivityHistory[]>([]);
        const showFilter = ref(false);

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
            // .finally(() => getFilterTypes(activitiesInTable.value))
        }

        // const getFilterTypes = (data: ICuratorActivityHistory[]) => {
        //     const filterKeys = ["activity_name", "uuid_to_fio", "description"];
        //     const filterObject: { activity_name?: string[], uuid_to_fio?: string[], description?: string[] } = {};
        //     filterKeys.forEach((e) => {
        //         data.forEach((i) => {
        //             if ((e as 'activity_name' | 'uuid_to_fio' | 'description') in filterObject && !(filterObject[e].includes(i[e as ('activity_name' | 'uuid_to_fio' | 'description') as keyof ICuratorActivityHistory]))) {
        //                 filterObject[(e as 'activity_name' | 'uuid_to_fio' | 'description')].push(i[e as keyof ICuratorActivityHistory])
        //             }
        //             else if (!(e in filterObject)) {
        //                 console.log(2);
        //                 filterObject[e as 'activity_name' | 'uuid_to_fio' | 'description'].push(i[e as keyof ICuratorActivityHistory])
        //             }
        //         })
        //     })
        //     console.log(filterObject);
        // }

        return {
            activitiesInTable,
            showFilter,
            moderate
        }
    }
})
</script>

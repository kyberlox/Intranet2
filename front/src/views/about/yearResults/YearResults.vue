<template>
    <div class="staff__filter__link d-flex gap-3 mt20">
        <RouterLink :to="{ name: 'year-results-id', params: { id: year } }"
                    v-for="(year, index) in actualYears"
                    :key="index">
            {{ year }}
        </RouterLink>
    </div>
    <div class="row mb-5 mt20">
        <h2 class="page__title">Сотрудник года ЭМК
            <span v-if="currentYear"
                  class="year">/ {{ currentYear }}</span>
        </h2>
        <WorkerCard :workers="workerOfTheYear" />
        <h2 v-if="workerWithDiploma.length"
            class="page__title mt20">
            Почетными грамотами награждены:
        </h2>
        <WorkerCard :workers="workerWithDiploma" />
    </div>
</template>
<script lang="ts">
import { onMounted, ref, watch, type Ref } from "vue";
import { defineComponent } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import WorkerCard from "./WorkerCard.vue";
import type { IWorkerOfTheYear } from "@/interfaces/IEntities";

export default defineComponent({
    props: {
        id: {
            type: String,
            default: null,
        },
    },
    components: {
        WorkerCard
    },
    setup(props) {
        const dateYear = new Date().getFullYear();
        const currentYear = ref(props.id ? props.id : dateYear - 1);

        const allTimeAwards: Ref<IWorkerOfTheYear[]> = ref([]);
        const chosenYearAwards: Ref<IWorkerOfTheYear[]> = ref([]);
        const workerOfTheYear: Ref<IWorkerOfTheYear[]> = ref([]);
        const workerWithDiploma: Ref<IWorkerOfTheYear[]> = ref([]);
        const actualYears: Ref<string[]> = ref([]);

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips["ДоскаПочета"]}`)
                .then(res => {
                    allTimeAwards.value.length = 0;
                    actualYears.value.length = 0;
                    allTimeAwards.value = res;
                    res.map((item: IWorkerOfTheYear) => {
                        if (item.indirect_data && (actualYears.value.length == 0 || (actualYears.value.indexOf(item.indirect_data.year) < 0))) {
                            actualYears.value.push(item.indirect_data.year)
                        }
                    })
                    actualYears.value.sort((a: string, b: string) => Number(a) - Number(b))
                })
                .finally(() => {
                    initWorkers();
                })
        })

        const initWorkers = () => {
            if (props.id) {
                currentYear.value = props.id;
            }
            chosenYearAwards.value.length = 0;
            workerWithDiploma.value.length = 0;
            workerOfTheYear.value.length = 0;

            allTimeAwards.value.map(item => {
                if (item.indirect_data && item.indirect_data.year == String(currentYear.value)) {
                    if (item.indirect_data.award == 'Почетная грамота') {
                        workerWithDiploma.value.push(item);
                    }
                    else {
                        workerOfTheYear.value.push(item);
                    }
                }
            })
        }

        watch(() => props.id, () => {
            initWorkers();
        }, {
            immediate: true
        })

        return {
            currentYear,
            chosenYearAwards,
            workerWithDiploma,
            workerOfTheYear,
            actualYears
        };
    },
});
</script>
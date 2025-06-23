<template>
    <div class="staff__filter__link d-flex gap-3 mt20">
        <RouterLink :to="{ name: 'year-results-id', params: { id: year } }"
                    v-for="(year, index) in Object.keys(workersOfTheYear)"
                    :key="index">
            {{ year }}
        </RouterLink>
    </div>

    <div class="row mb-5 mt20">
        <h2 class="page__title">Сотрудник года ЭМК
            <span v-if="currentYear"
                  class="year">/ {{ currentYear }}</span>
        </h2>
        <WorkerCard :workers="workerWithDiploma" />

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
import { workersOfTheYear } from "@/assets/static/workersOfTheYear";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import type { IWorkersResults } from "@/interfaces/IWorkersOfTheYear";
import WorkerCard from "./WorkerCard.vue";
import { renameKey } from "@/utils/renameKey";

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

        const allTimeAwards: Ref<IWorkersResults[]> = ref([]);
        const chosenYearAwards: Ref<IWorkersResults[]> = ref([]);
        const workerOfTheYear: Ref<IWorkersResults[]> = ref([]);
        const workerWithDiploma: Ref<IWorkersResults[]> = ref([]);

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips["ДоскаПочета"]}`)
                .then(res => {
                    const transformedData = res.map((item: IWorkersResults) => {
                        const newItem = { ...item };

                        if (newItem.PROPERTY_1035) {
                            renameKey(newItem.PROPERTY_1035, "year");
                        }
                        if (newItem.PROPERTY_1113) {
                            renameKey(newItem.PROPERTY_1113, "awardType");
                        }
                        return newItem;
                    });
                    allTimeAwards.value.length = 0;
                    allTimeAwards.value = transformedData;
                })
                .then(() => {
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
                if (item["PROPERTY_1035"] && item["PROPERTY_1035"]["year"] == String(currentYear.value)) {
                    if (item["PROPERTY_1113"] && item["PROPERTY_1113"]["awardType"] == "888") {
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
            workersOfTheYear,
            currentYear,
            chosenYearAwards,
            workerWithDiploma,
            workerOfTheYear
        };
    },
});
</script>
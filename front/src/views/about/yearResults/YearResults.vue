<template>
<div v-if="isLoading"
     class="contest__page__loader">
    <Loader />
</div>
<div v-else>
    <div v-if="workersLocations"
         class="tags">
        <div v-for="(location, index) in workersLocations"
             :key="'location' + index"
             class="tag__wrapper ">
            <div class="tags__tag tags__tag--nohover tags__tag--inner section__item__link btn-air"
                 :class="{ 'tags__tag--active': activeLocation == location }"
                 @click="activeLocation = location">
                {{ 'Доска почета ' + location }}
            </div>
        </div>
    </div>
    <div v-if="actualYears.length"
         class="staff__filter__link d-flex gap-3 mt20">
        <div v-for="(year, index) in actualYears"
             :key="index"
             :class="{ 'staff__filter__link--active': currentYear == Number(year) }"
             @click="currentYear = Number(year)">
            {{ year }}
        </div>
    </div>
    <div class="row mb-5 mt20"
         v-if="awardTypes.length && currentYear && activeLocation">
        <h2 class="page__title">
            {{ activeLocation }}
            <span v-if="currentYear"
                  class="year">/ {{ currentYear }}</span>
        </h2>

        <div class="mb-5"
             v-for="award in awardTypes"
             :key="award">
            <div v-if="awardFilter(allTimeAwards, award).length">
                <WorkerCard :pageTitle="award"
                            :workers="awardFilter(allTimeAwards, award)" />
            </div>
        </div>

    </div>
</div>
</template>
<script lang="ts">
import { onMounted, ref, watch, type Ref } from "vue";
import { defineComponent } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import WorkerCard from "./WorkerCard.vue";
import Loader from "@/components/layout/Loader.vue";
import type { IWorkerOfTheYear } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        WorkerCard,
        Loader
    },
    setup() {
        const currentYear = ref();
        const isLoading = ref(false);
        const workersLocations = ref<string[]>([]);
        const activeLocation = ref<string>();
        const awardTypes = ref<string[]>([]);

        const allTimeAwards: Ref<IWorkerOfTheYear[]> = ref([]);
        const chosenYearAwards: Ref<IWorkerOfTheYear[]> = ref([]);
        const actualYears: Ref<string[]> = ref([]);

        onMounted(() => {
            isLoading.value = true;
            Api.get(`article/find_by/${sectionTips["ДоскаПочета"]}`)
                .then(res => {
                    allTimeAwards.value.length = 0;
                    actualYears.value.length = 0;
                    allTimeAwards.value = res;
                    res.map((item: IWorkerOfTheYear) => {
                        if (item.indirect_data?.location && !workersLocations.value.includes(item.indirect_data?.location)) {
                            workersLocations.value.push(item.indirect_data.location);
                        }
                        activeLocation.value = workersLocations.value[0];
                        if (item.indirect_data?.year && !actualYears.value.includes(item.indirect_data.year)) {
                            actualYears.value.push(item.indirect_data.year)
                        }
                    })
                    currentYear.value = actualYears.value.sort((a, b) => Number(b) - Number(a))[0];
                })
                .finally(() => {
                    initWorkers();
                    isLoading.value = false;
                })
        })

        const initWorkers = (changeYear: boolean = false) => {
            chosenYearAwards.value.length = 0;
            awardTypes.value.length = 0
            actualYears.value.length = 0;
            allTimeAwards.value.map(item => {
                if (item.indirect_data?.location == activeLocation.value
                    && item.indirect_data
                    && (actualYears.value.length == 0
                        || !actualYears.value.includes(item.indirect_data.year))) {
                    actualYears.value.push(item.indirect_data.year)

                }
                if (item.indirect_data?.award
                    && !awardTypes.value.includes(item.indirect_data?.award)
                    && currentYear.value == item.indirect_data?.year
                    && activeLocation.value == item.indirect_data.location) {
                    awardTypes.value.push(item.indirect_data.award)
                }
            })
            actualYears.value.sort((a: string, b: string) => Number(a) - Number(b));
            if (!actualYears.value.includes(currentYear.value) && !changeYear) {
                currentYear.value = actualYears.value[actualYears.value.length - 1]
            }
        }

        watch((activeLocation), () => {
            initWorkers();
        }, { immediate: true, deep: true })

        watch((currentYear), () => {
            initWorkers(true);
        }, { immediate: true, deep: true })

        return {
            currentYear,
            chosenYearAwards,
            actualYears,
            isLoading,
            activeLocation,
            workersLocations,
            awardTypes,
            allTimeAwards,
            awardFilter: ((items: IWorkerOfTheYear[], award: string) =>
                items.filter((e) => e.indirect_data?.award == award
                    && e.indirect_data.year == currentYear.value && activeLocation.value == e.indirect_data.location))
        };
    },
});
</script>
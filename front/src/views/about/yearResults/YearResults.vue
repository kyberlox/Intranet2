<template>
<div v-if="isLoading"
     class="contest__page__loader__wrapper">
    <Loader class="contest__page__loader" />
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
                {{ location }}
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
    <div class="row mb-5 mt20">
        <h2 class="page__title">
            Сотрудник года {{ activeLocation }}
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
        const dateYear = new Date().getFullYear();
        const currentYear = ref(dateYear - 1);
        const isLoading = ref(false);
        const workersLocations = ref<string[]>([]);
        const activeLocation = ref<string>('ЭМК');

        const allTimeAwards: Ref<IWorkerOfTheYear[]> = ref([]);
        const chosenYearAwards: Ref<IWorkerOfTheYear[]> = ref([]);
        const workerOfTheYear: Ref<IWorkerOfTheYear[]> = ref([]);
        const workerWithDiploma: Ref<IWorkerOfTheYear[]> = ref([]);
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
                            workersLocations.value.push(item.indirect_data.location)
                        }
                    })
                })
                .finally(() => {
                    initWorkers();
                    isLoading.value = false;
                })
        })

        const initWorkers = () => {
            chosenYearAwards.value.length = 0;
            workerWithDiploma.value.length = 0;
            workerOfTheYear.value.length = 0;
            actualYears.value.length = 0;

            allTimeAwards.value.map(item => {
                if (item.indirect_data?.location == activeLocation.value && item.indirect_data && (actualYears.value.length == 0 || (actualYears.value.indexOf(item.indirect_data.year) < 0))) {
                    actualYears.value.push(item.indirect_data.year)
                }
                if (item.indirect_data && item.indirect_data.year == String(currentYear.value) && item.indirect_data.location == activeLocation.value) {
                    if (item.indirect_data.award == 'Почетная грамота') {
                        workerWithDiploma.value.push(item);
                    }
                    else {
                        workerOfTheYear.value.push(item);
                    }
                }
            })
            actualYears.value.sort((a: string, b: string) => Number(a) - Number(b))
        }

        watch((activeLocation), () => {
            initWorkers();
            currentYear.value = dateYear - 1;
        }, {
            immediate: true,
            deep: true
        })

        watch((currentYear), () => {
            initWorkers();
        }, {
            immediate: true,
            deep: true
        })

        return {
            currentYear,
            chosenYearAwards,
            workerWithDiploma,
            workerOfTheYear,
            actualYears,
            isLoading,
            activeLocation,
            workersLocations
        };
    },
});
</script>
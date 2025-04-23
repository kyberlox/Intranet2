<template>
    <div class="staff__filter__link d-flex gap-3 mt20">
        <RouterLink class=""
                    :to="{ name: 'year-results-id', params: { id: year } }"
                    v-for="(year, index) in Object.keys(workersOfTheYear)"
                    :key="index">{{ year }}</RouterLink>
    </div>

    <h2 class="page__title mt20">
        Сотрудник года ЭМК <span class="year"
              style="font-weight: 300">/ {{ currentYear }}</span>
    </h2>

    <div class="row mb-5 mt20">
        <div class="staff__item-wrapper col-sm-2"
             v-for="item in renderThisYearWorkers"
             :key="item.id">
            <div class="staff__item"
                 @click="
                    isOpen = true;
                workerInModal = item;
                ">
                <div>
                    <img class="img-fluid staff__item-img"
                         src="/src/assets/imgs/about/yearResults/gazinskii.png" />
                </div>
                <div class="staff__item-name">
                    {{ item.name }}
                </div>
                <div class="staff__item-position">{{ item.position }}</div>
                <div class="staff__item-organisation">{{ item.department }}</div>
            </div>
            <ResultModal :worker="workerInModal"
                         :isOpen="isOpen"
                         @closeModal="isOpen = false" />
        </div>
    </div>
</template>
<script lang="ts">
import { ref, watch } from "vue";
import { defineComponent } from "vue";
import { workersOfTheYear } from "@/assets/staticJsons/workersOfTheYear";
import ResultModal from "./ResultModal.vue";
export default defineComponent({
    props: {
        id: {
            type: Number,
            default: null,
        },
    },
    components: {
        ResultModal,
    },
    setup(props) {
        const currentYear = ref(props.id ? props.id : 2023);

        watch(
            () => props.id,
            () => {
                currentYear.value = props.id;
                renderThisYearWorkers.value = workersOfTheYear[props.id];
            }
        );

        const isOpen = ref(false);
        const workerInModal = ref();

        const renderThisYearWorkers = ref(workersOfTheYear[currentYear.value]);

        return {
            renderThisYearWorkers,
            workersOfTheYear,
            currentYear,
            isOpen,
            workerInModal,
        };
    },
});
</script>

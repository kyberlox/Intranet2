<template>
    <div class="trainings-table mt20">
        <div class="row">
            <TagDateNavBar @pickYear="pickYear"
                           :years="trainingYears"
                           :modifiers="'noTag'" />
        </div>
        <div class="trainings-table__filter__wrap mt20">
            <div class="row">
                <div class="col-12 col-md-12 col-lg-12 col-xl-5 d-flex align-items-center">
                    <span class="trainings-table__filter__row">Наименование</span>
                </div>
                <div v-if="page !== 'announces' && page !== 'literature'"
                     class="col-12 col-md-12 col-lg-12 col-xl-2 d-flex align-items-center">
                    <span class="trainings-table__filter__row">Оценка</span>
                </div>
                <div v-if="page !== 'literature'"
                     class="col-12 col-md-12 col-lg-12 col-xl-2 d-flex align-items-center">
                    <span class="trainings-table__filter__row">Дата</span>
                </div>
                <div v-if="page == 'literature'"
                     class="col-12 col-md-12 col-lg-12 col-xl-2 d-flex align-items-center">
                    <span class="trainings-table__filter__row">Описание</span>
                </div>
                <div class="col-12 col-md-12 col-lg-12 col-xl-2 d-flex align-items-center">
                    <span class="trainings-table__filter__row">Автор</span>
                </div>
            </div>
        </div>

        <div class="conducted-training__list__items">
            <div class="row">
                <div class="conducted-training__list__item col-12"
                     v-for="training in renderTrainings"
                     :key="training.id">
                    <RouterLink :to="{ name: 'training', params: { id: training.id } }"
                                title="Тимбилдинг САЗ"
                                class="conducted-training__list__item__top row pt-3 pb-3">
                        <div class="conducted-training__list__item__title col-12 col-md-12 col-lg-5 col-xl-5">
                            <h3 class="conducted-training__list__item__title__one">{{ training.title }}</h3>
                            <h4 v-if="training.subtitle"
                                class="conducted-training__list__item__title__two">{{ training.subtitle }}</h4>
                        </div>
                        <div v-if="page !== 'announces' && page !== 'literature'"
                             class="col-12 col-md-12 col-lg-2 col-xl-2 d-flex conducted-training__list__item__review">
                            <div class="score-stars"
                                 :class="[takeStarClass(training.score)]"></div>
                            <span v-if="training.reviewsCount"
                                  class="score-stars__count">({{ training.reviewsCount }})</span>
                        </div>
                        <div v-if="page !== 'literature'"
                             class="conducted-training__list__item__date col-12 col-md-12 col-lg-2 col-xl-2">{{
                                training.date }}</div>
                        <div v-if="page == 'literature'"
                             class="conducted-training__list__item__date col-12 col-md-12 col-lg-2 col-xl-2">{{
                                training.description }}</div>
                        <div class="conducted-training__list__item__author col-12 col-md-12 col-lg-3 col-xl-3">
                            <span>Автор курса:</span>
                            <span>{{ training.author }}</span>
                        </div>
                        <div v-if="page == 'literature'"
                             class="col-12 col-md-12 col-lg-2 col-xl-2">
                            <a :href="training.link"
                               class="conducted-training__list__item__download submit-button">Скачать</a>
                        </div>
                    </RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { ref, computed, defineComponent } from "vue";
import { conductedTrainings } from "@/assets/staticJsons/trainingCenterData";
import TagDateNavBar from "@/components/tools/common/TagDateNavBar.vue";

export default defineComponent({
    props: {
        page: {
            type: String,
            default: "conducted",
        },
    },
    components: {
        TagDateNavBar
    },
    setup() {
        const years = Object.keys(conductedTrainings).sort((a, b) => Number(b) - Number(a));
        const takeStarClass = (star: number | string) => {
            return `score-stars__${String(star)}`;
        };
        const renderYear = ref('2022');
        const pickYear = (year: string) => {
            renderYear.value = year;
        }

        return {
            renderYear,
            years,
            conductedTrainings,
            renderTrainings: computed(() => conductedTrainings[renderYear.value]),
            takeStarClass,
            pickYear,
            trainingYears: ['2022', '2021', '2020', '2019', '2018']
        };
    },
})
</script>

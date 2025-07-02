<template>
    <div v-if="tableElements"
         class="trainings-table mt20">

        <div class="trainings-table__filter__wrap mt20">
        </div>

        <div class="conducted-training__list__items">
            <div class="row">
                <div class="conducted-training__list__item col-12"
                     v-for="training in tableElements"
                     :key="training.id">
                    <div class="conducted-training__list__item__top row pt-3 pb-3">
                        <div class="conducted-training__list__item__title col-12 col-md-12 col-lg-5 col-xl-5">
                            <h3 class="conducted-training__list__item__title__one">{{ training.name }}</h3>
                            <h4 v-if="training.subsection"
                                class="conducted-training__list__item__title__two">{{ training.subsection }}</h4>
                            <span class="conducted-training__list__item__title__undertitle-author"
                                  v-if="page == 'literature'">{{ training.indirect_data.author }}</span>

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
                             class="conducted-training__list__item__date conducted-training__list__item__date--content col-12 col-md-12 col-lg-2 col-xl-2">
                            {{
                                training.content_text }}
                        </div>

                        <div v-if="page !== 'literature'"
                             class="conducted-training__list__item__author col-12 col-md-12 col-lg-3 col-xl-3">
                            <span>Автор курса:</span>
                            <span>{{ training.indirect_data.author }}</span>
                        </div>
                        <div v-if="page == 'literature'"
                             class="conducted-training__list__item__download col-12 col-md-12 col-lg-3 col-xl-3">
                            <a download
                               :href="training.documentation[0]?.file_url ?? training.images[0]?.file_url">Скачать.pdf</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { ref, computed, defineComponent, onMounted, watch } from "vue";

export default defineComponent({
    props: {
        page: {
            type: String,
            default: "conducted",
        },
        tableElements: {
            type: Array
        }
    },

    setup(props) {
        const conductedTrainings = ref({});
        const years = Object.keys(conductedTrainings).sort((a, b) => Number(b) - Number(a));
        const takeStarClass = (star: number | string) => {
            return `score-stars__${String(star)}`;
        };
        const renderYear = ref('2022');

        const pickFilter = (param: string) => {
            renderYear.value = param;
        }

        return {
            renderYear,
            years,
            conductedTrainings,
            takeStarClass,
            pickFilter,
        };
    },
})
</script>

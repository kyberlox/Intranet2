<template>
<div v-if="visibleTrainings"
     class="trainings-table mt20">

    <div v-if="page == 'conductedTrainings'"
         class="trainings-table__filter__wrap mt20">
        <button @click="showFilter = !showFilter"
                class="btn  dropdown-toggle tagDateNavBar__dropdown-toggle">
            Год публикации
        </button>
        <DateFilter v-if="showFilter"
                    @pickFilter="filterBy"
                    :params="years" />
    </div>

    <div class="conducted-training__list__items">
        <div class="row">
            <div class="conducted-training__list__item col-12"
                 v-for="training in visibleTrainings"
                 :key="training.id">
                <div class="conducted-training__list__item__top row pt-3 pb-3">
                    <div class="conducted-training__list__item__title col-12 col-md-12 col-lg-5 col-xl-5">
                        <h3 class="conducted-training__list__item__title__one">{{ training.name }}</h3>
                        <h4 v-if="training.subsection"
                            class="conducted-training__list__item__title__two">{{ training.subsection }}</h4>
                        <span class="conducted-training__list__item__title__undertitle-author">
                            {{ training.indirect_data?.author }}
                        </span>
                    </div>
                    <div v-if="page !== 'announces' && page !== 'literature'"
                         class="col-12 col-md-12 col-lg-2 col-xl-2 d-flex conducted-training__list__item__review">
                        <div v-if="training.indirect_data && training.indirect_data.reviews"
                             class="score-stars"
                             @click="openModal(training)"
                             :class="[takeStarClass(training.indirect_data.reviews)]"
                             style="cursor: pointer;"></div>
                        <span class="score-stars__count">({{ training.indirect_data?.reviews?.length || 0 }})</span>
                    </div>
                    <div v-if="page !== 'literature'"
                         class="conducted-training__list__item__date col-12 col-md-12 col-lg-2 col-xl-2">{{
                            training.date ?? training.indirect_data?.event_date }}</div>

                    <div class="conducted-training__list__item__date conducted-training__list__item__date--content col-12 col-md-12 col-lg-2 col-xl-2"
                         v-html="training.content_text">
                    </div>
                    <div v-if="page == 'literature'"
                         class="conducted-training__list__item__download col-12 col-md-12 col-lg-3 col-xl-3">
                        <a v-if="training.documentation?.length"
                           download
                           :href="training.documentation[0].file_url">Скачать в .pdf</a>
                        <a v-else-if="training.images?.length"
                           download
                           :href="training.images[0].file_url">
                            Скачать в .jpg
                        </a>
                        <a v-else-if="training.videos_native && training.videos_native.length"
                           download
                           :href="training.videos_native[0].file_url">
                            Скачать в .mp4
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { ref, defineComponent, watch, type Ref } from "vue";
import type { ItableItem } from "@/interfaces/IEntities";
import DateFilter from "@/components/tools/common/DateFilter.vue";
import { useRoute } from "vue-router";

export default defineComponent({
    props: {
        page: {
            type: String,
        },
        tableElements: {
            type: Array<ItableItem>,
        }
    },
    components: {
        DateFilter
    },
    setup(props, { emit }) {
        const visibleTrainings: Ref<ItableItem[]> = ref([]);
        const years: Ref<string[]> = ref([]);
        const route = useRoute();
        const showFilter = ref(false);
        const takeStarClass = (reviews: { stars?: string }[]) => {
            if (!reviews || !Array.isArray(reviews) || reviews.length === 0) {
                return 'score-stars__0';
            }

            let allStarsSum = 0;
            let validReviewsCount = 0;

            reviews.forEach((review) => {
                if (review.stars && typeof review.stars === 'string') {
                    const starValue = Number(review.stars);
                    if (!isNaN(starValue)) {
                        allStarsSum += starValue;
                        validReviewsCount++;
                    }
                }
            });

            if (validReviewsCount === 0) {
                return 'score-stars__0';
            }

            const averageStars = Math.round(allStarsSum / validReviewsCount);
            return `score-stars__${averageStars}`;
        };

        const openModal = (training: ItableItem) => {
            emit('openModal', training);
        };
        watch((props), (newVal) => {
            if (!newVal.tableElements) return
            if (route.name !== 'literature') {
                newVal.tableElements.forEach((e) => {
                    if (!e.indirect_data) return;
                    const target = e.indirect_data.event_date;
                    if (!target) return;
                    const newDate = target.split('.')[2];
                    if (newDate && !years.value.includes(newDate)) {
                        years.value.push(newDate)
                    }
                })
                years.value.sort((b: string, a: string) => { return Number(a) - Number(b) })
            }
            visibleTrainings.value = newVal.tableElements
        }, { immediate: true, deep: true })

        const filterBy = (param: string) => {
            if (!props.tableElements) return
            visibleTrainings.value = props.tableElements;
            visibleTrainings.value = visibleTrainings.value.filter((e) => { return e.indirect_data?.event_date ? e.indirect_data.event_date.split('.')[2] == param : '' })
            showFilter.value = false;
        }

        return {
            years,
            showFilter,
            visibleTrainings,
            takeStarClass,
            openModal,
            filterBy,
        };
    },
})
</script>

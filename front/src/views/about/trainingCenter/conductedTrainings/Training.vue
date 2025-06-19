<template>
    <div class="page__title mt20">Проведённые тренинги</div>
    <div class="conducted-training__detail__section">
        <div class="row">
            <div class="col-12 col-md-6">
                <div class="conducted-training__detail__content">
                    <div class="news__detail__top mb-4">
                        <h2 class="news__detail__title">{{ training.title }}</h2>
                        <RouterLink :to="{ name: 'conductedTrainings' }"
                                    class="news__detail__top__link"> К списку тренингов </RouterLink>
                    </div>

                    <div class="news__detail__discr"
                         v-html="training.description"></div>
                    <h3 v-if="training.materials"
                        class="news__detail__title mb-3">Материалы:</h3>
                    <div class="conducted-training__list__item__materials">
                        <a v-for="(material, index) in training.materials"
                           target="_blank"
                           :key="index"
                           :href="material.href"
                           class="conducted-training__list__item__materials__item">Скачать {{ material.title }}</a>
                    </div>

                    <div v-if="training.album">
                        <div class="col-6 d-flex align-items-center conducted-training__group-button">
                            <RouterLink :to="training.album"
                                        class="btn__link__metall"
                                        style="text-decoration: none">Смотреть фото</RouterLink>
                            <div class="btn__link__metall"
                                 style="text-decoration: none"
                                 @click="hiddenReviewModal = false">Добавить отзыв</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-6">
                <div class="col-6 d-flex justify-content-end pr-5 conducted-training__review__wrapper">
                    <div class="conducted-training__list__item__users__block"
                         @mouseenter="hiddenDropDown = false"
                         @mouseleave="hiddenDropDown = true">
                        <div class="conducted-training__list__item__users">
                            <div class="conducted-training__users__list">
                                <span v-for="(worker, index) in training.peoples"
                                      :key="index">
                                    <img :src="worker.img"
                                         alt="фото сотрудника" />
                                </span>
                                <span v-if="training.peoples.length > 3">+ {{ training.peoples.length - 3 }}</span>
                            </div>
                            <div class="conducted-training__users__list__full"
                                 :class="{ hidden: hiddenDropDown }">
                                <h5>Прошли тренинг</h5>
                                <div class="conducted-training__users__list__full__list scroll__cont">
                                    <span v-for="(worker, index) in training.peoples"
                                          :key="index">
                                        <img :src="worker.img"
                                             alt="фото сотрудника" />
                                        <span>{{ worker.name }}</span>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="conducted-training__review__section"
                     v-if="training.reviews">
                    <div class="accordion">
                        <div class="accordion__item"
                             v-for="(item, index) in training.reviews"
                             :key="index">
                            <details open
                                     class="accordion__details">
                                <summary class="accordion__summary">Отзыв № {{ index + 1 }}</summary>
                                <p class="accordion__title">{{ item }}</p>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
            <Transition name="modal">
                <ReviewForm v-if="!hiddenReviewModal"
                            @showToast="(text) => showToast(text)"
                            @closeModal="hiddenReviewModal = true" />
            </Transition>
            <Transition name="modal">
                <Toast v-if="!hiddenToast"
                       :toastText="toastText"
                       @closeToast="hiddenToast = true" />
            </Transition>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, ref } from "vue";
import ReviewForm from "@/views/about/trainingCenter/components/ReviewForm.vue";
import Toast from "@/components/tools/Toast.vue";
export default defineComponent({
    components: {
        ReviewForm,
        Toast,
    },
    setup() {
        const training = {
            title: 'Семинар-тренинг "Эффективная работа в команде"',
            description:
                "<p>В рамках тренинга участники практиковались в составлении модели создания и развития команды, проведении анализа сильных и слабых сторон командной работы, а также оценке действий лидера для достижения общих целей коллектива. Все сопровождалось практическими упражнениями и живой дискуссией.</p>",
            materials: [
                {
                    title: "Список литературы.pdf",
                    href: "www.google.com",
                },
            ],
            peoples: [
                {
                    name: "1",
                    img: "https://portal.emk.ru/upload/resize_cache/main/3a9/la6p0xocac50n4ai2i4bmu2pdeeeyyqf/32_32_2/%D0%94%D1%80%D1%83%D0%B7%D0%B8%D0%BD%D0%B0.jpg.png",
                },
            ],
            album: "www.google.com",
            reviews: ["1dadsasadsda", "2sadsada"],
        };

        const hiddenDropDown = ref(true);
        const hiddenReviewModal = ref(true);
        const hiddenToast = ref(true);
        const toastText = ref('');
        const showToast = (text: string) => {
            toastText.value = text;
            hiddenToast.value = false;
        };

        return {
            training,
            hiddenDropDown,
            hiddenReviewModal,
            toastText,
            hiddenToast,
            showToast,
        };
    },
});
</script>

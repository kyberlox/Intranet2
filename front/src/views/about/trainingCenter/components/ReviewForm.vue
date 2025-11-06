<template>
    <div class="modal__overlay">
        <div class="modal__wrapper modal__wrapper--review">
            <div class="modal__header">
                <h5 class="modal__title">Оставить отзыв</h5>
                <button class="modal__close-btn"
                        @click="closeModal"></button>
            </div>
            <div class="modal__body modal__body--review">
                <div class="modal__grid modal__grid--review">
                    <div class="modal__input__text">
                        <textarea class="modal__input__text__input"
                                  v-model="reviewText"
                                  :rows="textAreaRowsToContent(reviewText)"
                                  placeholder="Введите текст..." />
                    </div>
                    <div class="modal__input__score">
                        <p>Оценка</p>
                        <label v-for="item in grade"
                               :key="item">
                            <span> {{ item }} </span>
                            <input type="radio"
                                   name="reviewScore"
                                   class="modal__input__score__input"
                                   :value="item" />
                        </label>
                    </div>
                </div>
            </div>
            <div class="modal__footer">
                <div class="modal__footer__submit-button submit-button"
                     @click="handleReviewSubmit">Отправить</div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, ref } from "vue";
import { textAreaRowsToContent } from "@/utils/StringUtils.js";
export default defineComponent({
    name: 'reviewForm',
    emits: ['closeModal'],
    setup(props, { emit }) {
        const grade = [1, 2, 3, 4, 5];
        const handleReviewSubmit = () => {
            emit("closeModal");
        };
        const reviewText = ref('');
        return {
            grade,
            reviewText,
            closeModal: () => emit("closeModal"),
            handleReviewSubmit,
            textAreaRowsToContent
        };
    },
})
</script>

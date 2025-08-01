<template>
    <button v-if="!isBeginning || !isEnd"
            class="swiper-navigation__buttons-group__button swiper-navigation__buttons-group__button--prev"
            :class="[{ 'swiper-pagination__button--disabled': isBeginning }, { 'swiper-navigation__buttons-group__button--bottom': buttonsPos == 'bottom' }]"
            :disabled="isBeginning"
            @click="slidePrev">
        <ArrowLeft />
    </button>
    <button v-if="!isBeginning || !isEnd"
            class="swiper-navigation__buttons-group__button swiper-navigation__buttons-group__button--next"
            :class="[{ 'swiper-pagination__button--disabled': isEnd }, { 'swiper-navigation__buttons-group__button--bottom': buttonsPos == 'bottom' }]"
            @click="slideNext"
            :disabled="isEnd">
        <ArrowRight />
    </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ArrowLeft from "@/assets/icons/posts/SwiperNavArrowLeft.svg?component";
import ArrowRight from "@/assets/icons/posts/SwiperNavArrowRight.svg?component";

export default defineComponent({
    name: 'swiperButtons',
    props: {
        isBeginning: {
            type: Boolean
        },
        isEnd: {
            type: Boolean
        },
        buttonsPos: {
            type: String,
            default: 'center'
        }
    },
    components: {
        ArrowLeft,
        ArrowRight
    },
    setup(props, { emit }) {
        return {
            slidePrev: () => emit('slidePrev'),
            slideNext: () => emit('slideNext'),
        }
    }
})
</script>
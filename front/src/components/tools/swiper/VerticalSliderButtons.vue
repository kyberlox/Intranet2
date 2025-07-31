<template>
    <button v-if="!isBeginning || !isEnd"
            class="swiper-navigation__buttons-group__button swiper-navigation__buttons-group__button--prev"
            :class="{ 'swiper-pagination__button--disabled': isBeginning }"
            :disabled="isBeginning"
            @click="slidePrev">
        <ArrowLeft />
    </button>
    <button v-if="!isBeginning || !isEnd"
            class="swiper-navigation__buttons-group__button swiper-navigation__buttons-group__button--next"
            :class="{ 'swiper-pagination__button--disabled': isEnd }"
            @click="slideNext"
            :disabled="isEnd">
        <ArrowRight />
    </button>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import ArrowLeft from "@/assets/icons/posts/SwiperNavArrowLeft.svg?component";
import ArrowRight from "@/assets/icons/posts/SwiperNavArrowRight.svg?component";

export default defineComponent({
    name: 'verticalSliderButtons',
    props: {
        isBeginning: {
            type: Boolean
        },
        isEnd: {
            type: Boolean
        }
    },
    components: {
        ArrowLeft,
        ArrowRight
    },
    setup(props, { emit }) {
        return {
            slidePrev: computed(() => emit('slidePrev')),
            slideNext: computed(() => emit('slideNext')),
        }
    }
})
</script>
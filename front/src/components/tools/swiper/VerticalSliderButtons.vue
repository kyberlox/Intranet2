<template>
    <div class="swiper-navigation__buttons-group swiper-navigation__buttons-group--birthday"
         v-if="!isBeginning || !isEnd">
        <button class="swiper-navigation__buttons-group__button swiper-pagination__button--prev"
                :class="{ 'swiper-pagination__button--disabled': isBeginning }"
                @click="slidePrev"
                :disabled="isBeginning">
            <ArrowLeft />
        </button>
        <div class="swiper-navigation__buttons-group__pagination"></div>
        <button class="swiper-navigation__buttons-group__button swiper-pagination__button--next"
                :class="{ 'swiper-pagination__button--disabled': isEnd }"
                @click="slideNext"
                :disabled="isEnd">
            <ArrowRight />
        </button>
    </div>
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
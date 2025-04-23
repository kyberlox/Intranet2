<template>
    <div class="slider-wrapper full-width-slider__wrapper">
        <swiper class="full-width-slider"
                v-bind="sliderConfig"
                @swiper="swiperOn">
            <swiper-slide class="full-width-slider__slide"
                          v-for="(image, index) in images"
                          :key="'postImg' + index">
                <img class="full-width-slider__slide__img"
                     :src="image"
                     @click.stop="slideNext" />
            </swiper-slide>
        </swiper>

        <div class="full-width-slider__navigation-container"
             v-if="images.length > 1"
             @click.stop="slideNext">
            <div class="full-width-slider__navigation">
                <button class="full-width-slider__navigation__button full-width-slider__navigation__button--prev"
                        :class="{ 'full-width-slider__navigation__button--disabled': isBeginning }"
                        :disabled="isBeginning"
                        @click.stop="slidePrev">
                    <SwiperArrowLeft />
                </button>
                <button class="full-width-slider__navigation__button full-width-slider__navigation__button--next"
                        :class="{ 'full-width-slider__navigation__button--disabled': isEnd }"
                        :disabled="isEnd"
                        @click.stop="slideNext">
                    <SwiperArrowRight />
                </button>
            </div>
            <div class="pagination-container full-width-slider__pagination-container">
                <div class="swiper-navigation__buttons-group__pagination"></div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import SwiperArrowRight from "@/assets/icons/common/SwiperArrowRight.svg?component";
import SwiperArrowLeft from "@/assets/icons/common/SwiperArrowLeft.svg?component";
import { useSwiperconf } from "@/utils/useSwiperConf";

import { officialEventSlide } from "@/assets/staticJsons/officialEventsSlides";

export default defineComponent({
    components: {
        Swiper,
        SwiperSlide,
        SwiperArrowRight,
        SwiperArrowLeft,
    },
    props: {
        // images: {
        //     type: Array as PropType<string[]>,
        //     required: true,
        // },
        activeIndex: {
            type: Number,
            default: 0
        },
    },
    setup(props) {
        console.log(props);

        return {
            swiperOn: useSwiperconf('fullWidth', props.activeIndex).swiperOn,
            slideNext: useSwiperconf('fullWidth', props.activeIndex).slideNext,
            slidePrev: useSwiperconf('fullWidth', props.activeIndex).slidePrev,
            sliderConfig: useSwiperconf('fullWidth', props.activeIndex).sliderConfig,
            swiperInstance: useSwiperconf('fullWidth', props.activeIndex).swiperInstance,
            isEnd: useSwiperconf('fullWidth', props.activeIndex).isEnd,
            isBeginning: useSwiperconf('fullWidth', props.activeIndex).isBeginning,
            images: officialEventSlide.slides,
        };
    },
});
</script>
<style>
.full-width-slider__wrapper {
    height: 100%;
}
</style>
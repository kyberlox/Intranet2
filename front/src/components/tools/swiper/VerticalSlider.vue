<template>
    <swiper v-bind="sliderConfig"
            @swiper="swiperOn">
        <swiper-slide class="swiper--vertical-slide"
                      v-for="(slide, index) in slides"
                      :key="'vertSlide' + index">
            <img :src="slide.image" />
            <span class="birthday-icon"></span>
            <div class="swiper--vertical-slide__info"
                 v-if="page == 'birthdays'">
                <div class="swiper--vertical-slide__name vertical-title">{{ slide.name }}</div>
                <div class="swiper--vertical-slide__position vertical-subtitle">{{ slide.position ? slide.position : ""
                }}</div>
                <div class="swiper--vertical-slide__department">{{ slide.department ? slide.department : "" }}</div>
            </div>
        </swiper-slide>
    </swiper>

    <div v-if="slides.length >= 3"
         class="swiper-navigation__buttons-group">
        <button class="swiper-navigation__buttons-group__button swiper-pagination__button--prev"
                :class="{ 'swiper-pagination__button--disabled': isBeginning }"
                @click="slidePrev">
            <ArrowLeft />
        </button>
        <div class="swiper-navigation__buttons-group__pagination"></div>
        <button class="swiper-navigation__buttons-group__button swiper-pagination__button--next"
                :class="{ 'swiper-pagination__button--disabled': isEnd }"
                @click="slideNext">
            <ArrowRight />
        </button>
    </div>
</template>

<script lang="ts">
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/navigation";
import ArrowLeft from "@/assets/icons/posts/SwiperNavArrowLeft.svg?component";
import ArrowRight from "@/assets/icons/posts/SwiperNavArrowRight.svg?component";
import { defineComponent } from "vue";
import { useSwiperconf } from "@/utils/useSwiperConf";
export default defineComponent({
    components: {
        Swiper,
        SwiperSlide,
        ArrowLeft,
        ArrowRight,
    },
    props: {
        slides: {
            type: Object,
            required: true,
        },
        page: {
            type: String,
        },
    },
    setup() {

        return {
            swiperOn: useSwiperconf('vertical').swiperOn,
            slideNext: useSwiperconf('vertical').slideNext,
            slidePrev: useSwiperconf('vertical').slidePrev,
            sliderConfig: useSwiperconf('vertical').sliderConfig,
            swiperInstance: useSwiperconf('vertical').swiperInstance,
            isEnd: useSwiperconf('vertical').isEnd,
            isBeginning: useSwiperconf('vertical').isBeginning,
        };
    },
});
</script>

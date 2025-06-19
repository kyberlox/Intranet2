<template>
    <swiper v-bind="sliderConfig"
            @swiper="swiperOn">
        <swiper-slide class="swiper--vertical-slide"
                      v-for="(slide, index) in slides"
                      :key="'vertSlide' + index">
            <img class="swiper--vertical-slide-img"
                 :src="slide.image"
                 alt="фото сотрудника" />
            <span v-if="modifiers && modifiers.includes('birthday-icon')"
                  class="birthday-icon"></span>
            <div class="swiper--vertical-slide__info"
                 v-if="page == 'birthdays'">
                <div class="swiper--vertical-slide__name vertical-title">{{ slide.name ?? slide.user_fio }}</div>
                <div class="swiper--vertical-slide__position vertical-subtitle">{{ slide.position ? slide.position : ""
                    }}</div>
                <div v-for="(item, index) in slide.department"
                     :key="index + 'dep'"
                     class="swiper--vertical-slide__department">
                    {{ item }}
                </div>
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
        modifiers: {
            type: Array,
            default: () => ['birthday-icon']
        }
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

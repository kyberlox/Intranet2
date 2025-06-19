<template>
    <swiper v-bind="sliderConfig"
            @swiper="swiperOn">

        <swiper-slide v-for="(image, index) in images"
                      :class="{ 'swiper-slide--boxPhoto': sectionId == 32 }"
                      :key="'postImg' + index">
            <img :src="image"
                 alt="изображение слайдера"
                 @click.stop.prevent="activeIndex = index; modalIsVisible = true" />
        </swiper-slide>

    </swiper>
    <div class="swiper-navigation__buttons-group"
         v-if="images.length > 1">
        <button class="swiper-navigation__buttons-group__button swiper-pagination__button--prev"
                :class="{ 'swiper-pagination__button--disabled': isBeginning }"
                @click.stop="slidePrev">
            <ArrowLeft />
        </button>
        <div class="swiper-navigation__buttons-group__pagination"></div>
        <button class="swiper-navigation__buttons-group__button swiper-pagination__button--next"
                :class="{ 'swiper-pagination__button--disabled': isEnd }"
                @click.stop="slideNext">
            <ArrowRight />
        </button>
    </div>
    <ZoomModal v-if="modalIsVisible"
               :image="images"
               :activeIndex="activeIndex"
               @close="modalIsVisible = false" />
</template>

<script lang="ts">
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import ArrowLeft from "@/assets/icons/posts/SwiperNavArrowLeft.svg?component";
import ArrowRight from "@/assets/icons/posts/SwiperNavArrowRight.svg?component";
import { repairVideoUrl } from "@/utils/embedVideoUtil";
import { defineComponent, type PropType, ref } from "vue";
import ZoomModal from '@/components/tools/modal/ZoomModal.vue';

import { useSwiperconf } from "@/utils/useSwiperConf";
export default defineComponent({
    components: {
        Swiper,
        SwiperSlide,
        ArrowLeft,
        ArrowRight,
        ZoomModal
    },
    props: {
        images: {
            type: Array as PropType<string[]>,
            required: true,
        },
        videos: {
            type: Array as PropType<string[]>,
            default: () => [],
        },
        type: {
            type: String,
            default: "common",
        },
        sectionId: {
            type: Number,
        }
    },
    setup(props) {
        const modalIsVisible = ref(false);
        const activeIndex = ref(0);
        return {
            swiperOn: useSwiperconf(props.type).swiperOn,
            slideNext: useSwiperconf(props.type).slideNext,
            slidePrev: useSwiperconf(props.type).slidePrev,
            sliderConfig: useSwiperconf(props.type).sliderConfig,
            swiperInstance: useSwiperconf(props.type).swiperInstance,
            isEnd: useSwiperconf(props.type).isEnd,
            isBeginning: useSwiperconf(props.type).isBeginning,
            repairVideoUrl,
            modalIsVisible,
            activeIndex
        };
    },
})
</script>

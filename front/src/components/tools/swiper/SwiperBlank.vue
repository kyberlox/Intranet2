<template>
    <swiper :class="{ 'swiper--inner': type == 'postInner' }"
            v-bind="sliderConfig"
            @swiper="swiperOn">
        <template v-if="type === 'postInner' && videos?.length">
            <swiper-slide v-for="(video, index) in videos"
                          :key="'postVideo' + index">
                <iframe width="100%"
                        height="500px"
                        :src="String(repairVideoUrl(video))"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen> </iframe>
            </swiper-slide>
        </template>

        <swiper-slide v-for="(image, index) in images"
                      :key="'postImg' + index">
            <img :src="image" />
        </swiper-slide>

    </swiper>
    <div v-if="type == 'postInner' && swiperInstance?.isBeginning !== swiperInstance?.isEnd"
         class="swiper-navigation__buttons-group">
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
</template>

<script lang="ts">
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import ArrowLeft from "@/assets/icons/posts/SwiperNavArrowLeft.svg?component";
import ArrowRight from "@/assets/icons/posts/SwiperNavArrowRight.svg?component";
import { repairVideoUrl } from "@/utils/embedVideoUtil";
import { defineComponent } from "vue";
import type { PropType } from "vue";

import { useSwiperconf } from "@/utils/useSwiperConf";
export default defineComponent({
    components: {
        Swiper,
        SwiperSlide,
        ArrowLeft,
        ArrowRight,
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
    },
    setup(props) {
        return {
            swiperOn: useSwiperconf(props.type).swiperOn,
            slideNext: useSwiperconf(props.type).slideNext,
            slidePrev: useSwiperconf(props.type).slidePrev,
            sliderConfig: useSwiperconf(props.type).sliderConfig,
            swiperInstance: useSwiperconf(props.type).swiperInstance,
            isEnd: useSwiperconf(props.type).isEnd,
            isBeginning: useSwiperconf(props.type).isBeginning,
            repairVideoUrl
        };
    },
})
</script>

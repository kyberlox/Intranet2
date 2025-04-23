<template>
    <div class="home__view__grid__card home__view__grid__card--soloblock d-flex flex-column">
        <div class="home__view__grid__card__group-title">{{ card.title }}</div>
        <div class="home__view__grid__card__image">
            <swiper v-bind="sliderConfig"
                    @swiper="swiperOn">
                <swiper-slide v-for="(slide, index) in card.images"
                              :key="'postImg' + index"
                              class="home__view__grid__card__image__swiper-slide">
                    <RouterLink class="
                                home__view__grid__card__link
                                home__view__grid__card__bg-image"
                                :to="{ name: card.href ?? slide.href }"
                                :style="{ backgroundImage: `url(${slide.image ?? 'https://placehold.co/360x206'})` }" />
                </swiper-slide>
            </swiper>
        </div>
    </div>
</template>

<script lang="ts">
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import { repairVideoUrl } from "@/utils/embedVideoUtil";
import { defineComponent } from "vue";
import { RouterLink } from "vue-router";
import { useSwiperconf } from "@/utils/useSwiperConf";

export default defineComponent({
    components: {
        Swiper,
        SwiperSlide,
        RouterLink
    },
    props: {
        card: {
            type: Object,
            required: true,
        }
    },
    setup(props) {
        console.log(props)
        return {
            swiperOn: useSwiperconf('main').swiperOn,
            slideNext: useSwiperconf('main').slideNext,
            slidePrev: useSwiperconf('main').slidePrev,
            sliderConfig: useSwiperconf('main').sliderConfig,
            swiperInstance: useSwiperconf('main').swiperInstance,
            isEnd: useSwiperconf('main').isEnd,
            isBeginning: useSwiperconf('main').isBeginning,
            repairVideoUrl
        };
    },
})
</script>
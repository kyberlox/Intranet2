<template>
    <div class="homeview__grid__card homeview__grid__card--soloblock d-flex flex-column">
        <RouterLink :to="{ name: card.href }"
                    class="homeview__grid__card__group-title">
            {{ card.title }}
        </RouterLink>
        <div class="homeview__grid__card__image">
            <swiper v-bind="sliderConfig"
                    @swiper="swiperOn">
                <swiper-slide v-if="!card.images.length"
                              v-lazy-load="chooseImgPlug()"
                              class="homeview__grid__card__bg-image homeview__grid__card__bg-image--plug">
                </swiper-slide>
                <swiper-slide v-else
                              v-for="(slide, index) in card.images"
                              :key="'postImg' + index"
                              class="homeview__grid__card__image__swiper-slide">
                    <RouterLink v-if="slide.image"
                                class="homeview__grid__card__link
                                homeview__grid__card__bg-image"
                                :to="{ name: card.href ?? slide.href }"
                                v-lazy-load="slide.image" />
                    <div v-else
                         class="homeview__grid__card__bg-image homeview__grid__card__bg-image--plug"
                         v-lazy-load="chooseImgPlug()">
                    </div>
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
import { chooseImgPlug } from "@/utils/chooseImgPlug";

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
    setup() {
        return {
            swiperOn: useSwiperconf('main').swiperOn,
            slideNext: useSwiperconf('main').slideNext,
            slidePrev: useSwiperconf('main').slidePrev,
            sliderConfig: useSwiperconf('main').sliderConfig,
            swiperInstance: useSwiperconf('main').swiperInstance,
            isEnd: useSwiperconf('main').isEnd,
            isBeginning: useSwiperconf('main').isBeginning,
            repairVideoUrl,
            chooseImgPlug
        };
    },
})
</script>
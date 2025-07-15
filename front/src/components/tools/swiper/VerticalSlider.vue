<template>
    <swiper class="swiper--vertical"
            v-bind="sliderConfig"
            @swiper="swiperOn">
        <swiper-slide class="swiper--vertical-slide"
                      v-for="(slide, index) in slides"
                      :key="'vertSlide' + index">

            <div class="swiper--vertical__bg-slide"
                 :style="{ backgroundImage: `url('${slide.preview_file_url ?? slide.image}')` }">

                <!-- Под технику безопасности-->
                <div v-if="page == 'safetyTechnics' || (modifiers && modifiers.includes('needLogo'))"
                     class="section__image__list__item__banner">
                    <span class="section__image__list__item__banner__inner">
                        <span v-if="page == 'safetyTechnics'"
                              class="section__image__list__item__category">
                            {{ slide.header }}
                        </span>
                        <div class="section__image__list__item__logo">
                            <img src="/src/assets/imgs/emkLogo.webp"
                                 alt="ЭМК"
                                 title="ЭМК" />
                        </div>
                        <h3 v-if="page !== 'care'"
                            class="section__image__list__item__title">{{ slide.name }}</h3>
                        <RouterLink v-if="page == 'safetyTechnics' || page == 'care'"
                                    :to="{ name: slide.routeTo ?? routeTo, params: { id: slide.id } }"
                                    class="section__image__list__item__link">
                            Читать
                        </RouterLink>
                    </span>
                </div>
                <div class="section__image__list__item__subtitle__wrapper">
                    <div class="section__image__list__item__subtitle vertical-title">
                        {{ slide.subtitle ?? slide.name }}
                    </div>
                    <div v-if="slide.description"
                         class="section__image__list__item__subtitle vertical-subtitle">
                        {{ slide.description }}
                    </div>
                    <div v-if="slide.indirect_data?.organizer"
                         class="section__image__list__item__subtitle vertical-subtitle">
                        {{ 'Организатор: ' + slide.indirect_data?.organizer }}
                    </div>
                </div>
            </div>
        </swiper-slide>
    </swiper>
</template>

<script lang="ts">
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/navigation";
import { defineComponent } from "vue";
import { useSwiperconf } from "@/utils/useSwiperConf";
import { type IVerticalSlide } from "@/interfaces/IVerticalSlide";


export default defineComponent({
    components: {
        Swiper,
        SwiperSlide,
    },
    props: {
        slides: {
            type: Array<IVerticalSlide>,
            required: true,
        },
        page: {
            type: String,
        },
        modifiers: {
            type: Array,
        },
        routeTo: {
            type: String
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

<style scoped>
.swiper {
    height: 100%;
}

.swiper--vertical-slide__department {
    max-width: 150px;
}
</style>
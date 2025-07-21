<template>
    <swiper class="swiper--vertical"
            v-bind="sliderConfig"
            @swiper="swiperOn">
        <swiper-slide class="swiper--vertical-slide"
                      :class="{ 'swiper--vertical-slide--care': page == 'care' }"
                      v-for="(slide, index) in slides"
                      :key="'vertSlide' + index">

            <div :class="{ 'swiper--vertical__bg-slide': page !== 'care' }"
                 :style="{ backgroundImage: `url('${slide.preview_file_url}')` }">
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
    </swiper>
</template>

<script lang="ts">
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/navigation";
import { defineComponent } from "vue";
import { useSwiperconf } from "@/utils/useSwiperConf";
import ArrowLeft from "@/assets/icons/posts/SwiperNavArrowLeft.svg?component";
import ArrowRight from "@/assets/icons/posts/SwiperNavArrowRight.svg?component";

interface IVerticalSlide {
    header?: string,
    preview_file_url?: string,
    name?: string,
    user_fio?: string,
    position?: string,
    department?: string,
    routeTo?: string,
    id?: number,
    subtitle?: string,
    description?: string,
    indirect_data?: {
        organizer?: string,

        // для благотворительных
        PROPERTY_342?: string[],
        PROPERTY_343?: string[],
        PROPERTY_344?: string[],
        PROPERTY_435?: string[],
        PROPERTY_347?: string[],
        PROPERTY_348?:
        {
            TYPE?: string,
            TEXT?: string
        }[],
        PROPERTY_349?: string[],
    }
}

export default defineComponent({
    components: {
        Swiper,
        SwiperSlide,
        ArrowLeft,
        ArrowRight
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
        const swiperConf = useSwiperconf('vertical');

        return {
            swiperOn: swiperConf.swiperOn,
            slideNext: swiperConf.slideNext,
            slidePrev: swiperConf.slidePrev,
            sliderConfig: swiperConf.sliderConfig,
            swiperInstance: swiperConf.swiperInstance,
            isEnd: swiperConf.isEnd,
            isBeginning: swiperConf.isBeginning,
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

.swiper--vertical-slide--care {
    height: min-content !important;
}
</style>
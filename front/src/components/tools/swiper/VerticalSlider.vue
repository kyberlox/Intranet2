<template>
    <swiper class="swiper--vertical"
            v-bind="sliderConfig"
            @swiper="swiperOn">
        <swiper-slide class="swiper--vertical-slide"
                      v-for="(slide, index) in slides"
                      :key="'vertSlide' + index">

            <div class="swiper--vertical__bg-slide"
                 :style="{ backgroundImage: `url('${slide.image}')` }">
                <span v-if="modifiers && modifiers.includes('birthday-icon')"
                      class="birthday-icon"></span>
                <!-- Под дни рождения -->
                <div class="swiper--vertical-slide__info"
                     v-if="page == 'birthdays'">
                    <div class="swiper--vertical-slide__name vertical-title">{{ slide.name ?? slide.user_fio }}</div>
                    <div class="swiper--vertical-slide__position vertical-subtitle">
                        {{ slide.position ? slide.position : "" }}
                    </div>
                    <div v-for="(item, index) in slide.department"
                         :key="index + 'dep'"
                         class="swiper--vertical-slide__department">
                        {{ item }}
                    </div>
                </div>
                <!-- Под технику безопасности-->
                <div v-else-if="page == 'safetyTechnics' || (modifiers && modifiers.includes('needLogo'))"
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
                        <h3 class="section__image__list__item__title">{{ slide.name }}</h3>
                        <RouterLink v-if="page == 'safetyTechnics'"
                                    :to="{ name: slide.routeTo, params: { id: slide.id } }"
                                    class="section__image__list__item__link">
                            Читать
                        </RouterLink>
                    </span>
                </div>
                <div class="section__image__list__item__subtitle__wrapper">
                    <div class="section__image__list__item__subtitle vertical-title">
                        {{ slide.subtitle }}
                    </div>
                    <div class="section__image__list__item__subtitle vertical-subtitle">
                        {{ slide.description }}
                    </div>
                </div>
            </div>
        </swiper-slide>
    </swiper>

    <div v-if="slides.length >= 3 && page == 'birthdays'"
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
import type { ISafetyTechnicsSlide } from "@/interfaces/IEntities";
export default defineComponent({
    components: {
        Swiper,
        SwiperSlide,
        ArrowLeft,
        ArrowRight,
    },
    props: {
        slides: {
            type: Object || ISafetyTechnicsSlide,
            required: true,
        },
        page: {
            type: String,
        },
        modifiers: {
            type: Array,
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
<style lang="scss">
.swiper--vertical {
    &>.swiper-wrapper {
        justify-content: space-around;
    }
}

.swiper--vertical-slide {
    max-width: 100% !important;
}

.swiper--vertical-slide img {
    object-fit: cover;
}

.swiper--vertical__bg-slide {
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    position: relative;
    overflow: hidden;
    aspect-ratio: auto;
    height: 100% !important;
    width: 100%;
    transition: var(--default-transition);
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}

.section__image__list__item__logo {
    max-height: 100px;
}

.section__image__list__item__subtitle__wrapper {

    font-weight: 600;
    font-size: 16px;
    line-height: 16px;
    color: #000000;
    width: 100%;
    background: rgb(255 255 255 / 88%);
    padding: 10px;

}

.section__image__list__item__title {
    max-width: 350px;
}

.section__image__list__item__banner {
    padding: 0px;
    gap: 15px;
}

.vertical-subtitle {
    color: rgba(0, 0, 0, 0.693);
}
</style>
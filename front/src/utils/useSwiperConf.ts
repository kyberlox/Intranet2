import type { Swiper as SwiperType } from 'swiper';
import { Navigation, Autoplay, Pagination } from "swiper/modules";

import { ref } from 'vue';

let swiperInstance: SwiperType | null = null;

const isBeginning = ref(true);
const isEnd = ref(false);

export const useSwiperconf = (type: string, activeIndex?: number) => {
    const swiperOn = (swiper: SwiperType) => {
        swiperInstance = swiper;
        isBeginning.value = swiperInstance.isBeginning;
        isEnd.value = swiperInstance.isEnd;

        swiperInstance.on("slideChange", () => {
            if (swiperInstance) {
                isBeginning.value = swiperInstance.isBeginning;
                isEnd.value = swiperInstance.isEnd;
            }
        });
    };

    const slideNext = () => {
        swiperInstance?.slideNext();
        if (swiperInstance) {
            isBeginning.value = swiperInstance.isBeginning;
            isEnd.value = swiperInstance.isEnd;
        }

    };
    const slidePrev = () => {
        if (swiperInstance) {
            swiperInstance?.slidePrev();
            isBeginning.value = swiperInstance.isBeginning;
            isEnd.value = swiperInstance.isEnd;
        }
    };

    const slidesPerViewDefine = (type: string) => {
        switch (type) {
            case 'fullWidth':
                return 1;
            case 'vertical':
                return 3;
            default:
                return "auto" as const;
        }
    }

    const sliderConfig = {
        modules: type == 'vertical' ? [Navigation, Autoplay] : [Navigation, Autoplay, Pagination],
        slidesPerView: slidesPerViewDefine(type),
        initialSlide: type == 'fullWidth' ? activeIndex : 0,
        spaceBetween: type == 'main' ? 2 : 12,
        autoplay:
            type !== "postInner"
                ? {
                    delay: 3000,
                    disableOnInteraction: false,
                    pauseOnMouseEnter: true,
                }
                : false,
        pagination: { el: ".swiper-navigation__buttons-group__pagination", clickable: true },
        navigation: {
            nextEl: type == 'fullWidth' ?
                ".full-width-slider-pagination__button--next" : ".swiper-navigation__buttons-group__button--next",
            prevEl: type == 'fullWidthSlider' ?
                "full-width-slider-pagination__button--prev" : ".swiper-navigation__buttons-group__button--prev",
        },
    };

    return {
        swiperOn,
        slideNext,
        slidePrev,
        sliderConfig,
        swiperInstance,
        isBeginning,
        isEnd,
    }
} 
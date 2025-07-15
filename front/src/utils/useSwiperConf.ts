import type { Swiper as SwiperType } from 'swiper';
import { Navigation, Autoplay, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";

import { nextTick, ref } from 'vue';

export const useSwiperconf = (type: string, activeIndex?: number) => {
    const swiperInstance = ref<SwiperType | null>(null);
    const isBeginning = ref(true);
    const isEnd = ref(false);

    const swiperOn = (swiper: SwiperType) => {
        console.log(swiper);

        swiperInstance.value = swiper;

        nextTick(() => {
            if (swiperInstance.value) {
                isBeginning.value = swiperInstance.value.isBeginning;
                isEnd.value = swiperInstance.value.isEnd;
                console.log(isBeginning);
                console.log(isEnd);

            }
        });

        swiper.on("slideChange", () => {
            if (swiperInstance.value) {
                isBeginning.value = swiperInstance.value.isBeginning;
                isEnd.value = swiperInstance.value.isEnd;
            }
        });
    };

    const slideNext = () => {
        console.log(swiperInstance);

        swiperInstance.value?.slideNext();
        if (swiperInstance.value) {
            isBeginning.value = swiperInstance.value.isBeginning;
            isEnd.value = swiperInstance.value.isEnd;
        }
    };

    const slidePrev = () => {
        if (swiperInstance.value) {
            swiperInstance.value.slidePrev();
            isBeginning.value = swiperInstance.value.isBeginning;
            isEnd.value = swiperInstance.value.isEnd;
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
        modules: type == 'vertical' ? [Navigation, Pagination] : [Navigation, Autoplay, Pagination],
        slidesPerView: slidesPerViewDefine(type),
        initialSlide: type == 'fullWidth' ? activeIndex : 0,
        spaceBetween: type == 'main' ? 2 : 12,
        speed: 0,
        autoplay:
            type !== "postInner"
                ? {
                    delay: 3000,
                    disableOnInteraction: false,
                }
                : false,
        breakpoints: {
            320: {
                slidesPerView: 1,
                spaceBetween: 8
            },
            480: {
                slidesPerView: 1,
                spaceBetween: 10
            },
            768: {
                slidesPerView: 1,
                spaceBetween: 12,
            },
            1024: {
                slidesPerView: 1,
                spaceBetween: 16
            },
            1200: {
                slidesPerView: 2,
                spaceBetween: 12
            },
            1400: {
                slidesPerView: 3,
            },
            1800: {
                slidesPerView: 3,
            }
        }
    };

    return {
        swiperOn,
        slideNext,
        slidePrev,
        sliderConfig,
        swiperInstance,
        isEnd,
        isBeginning
    };
};

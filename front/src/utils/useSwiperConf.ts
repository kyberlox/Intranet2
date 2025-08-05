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
        swiperInstance.value = swiper;

        nextTick(() => {
            if (swiperInstance.value) {
                isBeginning.value = swiperInstance.value.isBeginning;
                isEnd.value = swiperInstance.value.isEnd;
            }
        });

        swiper.on("update", () => {
            if (swiperInstance.value) {
                isBeginning.value = swiperInstance.value.isBeginning;
                isEnd.value = swiperInstance.value.isEnd;
            }
        })

        swiper.on("slideChange", () => {
            if (swiperInstance.value) {
                isBeginning.value = swiperInstance.value.isBeginning;
                isEnd.value = swiperInstance.value.isEnd;
            }
        });

        swiper.on("breakpoint", () => {
            nextTick(() => {
                if (swiperInstance.value) {
                    isBeginning.value = swiperInstance.value.isBeginning;
                    isEnd.value = swiperInstance.value.isEnd;
                }
            })
        })
    };

    const slideNext = () => {
        swiperInstance.value?.slideNext();
    };

    const slidePrev = () => {
        swiperInstance.value?.slidePrev();
    };

    const slidesPerViewDefine = (type: string) => {
        switch (type) {
            case 'fullWidth':
                return 1;
            case 'vertical':
                return 3;
            case 'newWorkers':
                return 4;
            default:
                return "auto" as const;
        }
    }

    const getBreakpoints = (type: string) => {
        switch (type) {
            case 'vertical':
                return {
                    320: {
                        slidesPerView: 1,
                        spaceBetween: 8
                    },
                    480: {
                        slidesPerView: 1,
                        spaceBetween: 10
                    },
                    768: {
                        slidesPerView: 2,
                        spaceBetween: 12,
                    },
                    1024: {
                        slidesPerView: 2,
                        spaceBetween: 16
                    },
                    1200: {
                        slidesPerView: 2,
                        spaceBetween: 12
                    },
                    1400: {
                        slidesPerView: 2,
                    },
                    1920: {
                        slidesPerView: 3
                    }
                }
            default:
                break;
        }
    }

    const sliderConfig = {
        modules: type == 'vertical' ? [Navigation, Pagination] : [Navigation, Autoplay, Pagination],
        slidesPerView: slidesPerViewDefine(type),
        initialSlide: type == 'fullWidth' ? activeIndex : 0,
        spaceBetween: type == 'main' ? 2 : 12,
        autoplay:
            type !== "postInner"
                ? {
                    delay: 3000,
                    disableOnInteraction: false,
                }
                : false,
        breakpoints: getBreakpoints(type)
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

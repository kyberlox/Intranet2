import type { Swiper as SwiperType } from 'swiper';
import { Navigation, Autoplay, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";

import { ref } from 'vue';

export const useSwiperconf = (type: string, activeIndex?: number) => {
    // Создаем локальные реактивные переменные для каждого экземпляра
    const swiperInstance = ref<SwiperType | null>(null);
    const isBeginning = ref(true);
    const isEnd = ref(false);

    const swiperOn = (swiper: SwiperType) => {
        swiperInstance.value = swiper;
        isBeginning.value = swiper.isBeginning;
        isEnd.value = swiper.isEnd;

        swiper.on("slideChange", () => {
            if (swiperInstance.value) {
                isBeginning.value = swiperInstance.value.isBeginning;
                isEnd.value = swiperInstance.value.isEnd;
            }
        });
    };

    const slideNext = () => {
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
        modules: type == 'vertical' ? [Navigation, Autoplay] : [Navigation, Autoplay, Pagination],
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
        // добавьте остальные настройки
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

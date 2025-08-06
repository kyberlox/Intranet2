<template>
    <div class="slider-wrapper full-width-slider__wrapper">
        <swiper class="full-width-slider"
                v-bind="sliderConfig"
                @swiper="onSwiperInit">
            <swiper-slide class="full-width-slider__slide"
                          v-for="(image, index) in images"
                          :key="'postImg' + index">
                <img class="full-width-slider__slide__img"
                     :src="getImageUrl(image)"
                     @click.stop="slideNext"
                     alt="слайд" />
            </swiper-slide>
        </swiper>

        <div class="full-width-slider__navigation-container"
             v-if="Array.isArray(images) && images.length > 1"
             @click.stop="slideNext">
            <div class="full-width-slider__navigation">
                <button class="full-width-slider__navigation__button full-width-slider__navigation__button--prev"
                        :class="{ 'full-width-slider__navigation__button--disabled': isBeginning }"
                        :disabled="isBeginning"
                        @click.stop="slidePrev">
                    <SwiperArrowLeft />
                </button>
                <button class="full-width-slider__navigation__button full-width-slider__navigation__button--next"
                        :class="{ 'full-width-slider__navigation__button--disabled': isEnd }"
                        :disabled="isEnd"
                        @click.stop="slideNext">
                    <SwiperArrowRight />
                </button>
            </div>
            <div class="pagination-container full-width-slider__pagination-container">
                <div class="swiper-navigation__buttons-group__pagination"></div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from "vue";
import { Swiper, SwiperSlide } from "swiper/vue";
import type { Swiper as SwiperType } from 'swiper';
import { Navigation, Autoplay, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import SwiperArrowRight from "@/assets/icons/common/SwiperArrowRight.svg?component";
import SwiperArrowLeft from "@/assets/icons/common/SwiperArrowLeft.svg?component";

interface ImageObject {
    file_url?: string;
}

type ImageItem = string | ImageObject;
type ImageArray = ImageItem[];

export default defineComponent({
    components: {
        Swiper,
        SwiperSlide,
        SwiperArrowRight,
        SwiperArrowLeft,
    },
    props: {
        images: {
            type: Array as PropType<ImageArray>,
        },
        activeIndex: {
            type: Number,
        },
    },
    setup(props) {
        const swiperInstance = ref<SwiperType | null>(null);
        const isBeginning = ref(true);
        const isEnd = ref(false);

        const onSwiperInit = (swiper: SwiperType) => {
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
            swiperInstance.value?.slidePrev();
            if (swiperInstance.value) {
                isBeginning.value = swiperInstance.value.isBeginning;
                isEnd.value = swiperInstance.value.isEnd;
            }
        };

        const sliderConfig = {
            modules: [Navigation, Autoplay, Pagination],
            slidesPerView: 1,
            initialSlide: props.activeIndex,
            spaceBetween: 12,
            autoplay: false,
        };

        const getImageUrl = (image: ImageItem): string => {
            if (typeof image === 'object' && image && 'file_url' in image && typeof image.file_url == 'string') {
                return image.file_url;
            }
            return image as string;
        };

        return {
            onSwiperInit,
            slideNext,
            slidePrev,
            sliderConfig,
            swiperInstance,
            isEnd,
            isBeginning,
            getImageUrl
        };
    },
});
</script>

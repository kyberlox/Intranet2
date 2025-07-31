<template>
    <swiper v-bind="sliderConfig"
            @swiper="swiperOn">

        <!-- для img -->
        <swiper-slide v-for="(image, index) in images"
                      :class="{ 'swiper-slide--boxPhoto': sectionId == 32 }"
                      :key="'postImg' + index">
            <img :src="typeof image == 'object' && 'file_url' in image ? image.file_url : image"
                 alt="изображение слайдера"
                 @click.stop.prevent="activeIndex = index; modalIsVisible = true" />
        </swiper-slide>

        <!-- для video -->
        <swiper-slide v-for="(video, index) in videos"
                      :key="'postVideo' + index">
            <iframe width="100%"
                    height="500px"
                    :title="'Видеоконтент'"
                    :src="String(repairVideoUrl(video))"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
            </iframe>
        </swiper-slide>

    </swiper>
    <div class="swiper-navigation__buttons-group"
         v-if="(images && images.length > 1) || (videos && videos.length > 1) || images && videos && images.length + videos.length > 1">
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
    <ZoomModal v-if="modalIsVisible"
               :image="images"
               :activeIndex="activeIndex"
               @close="modalIsVisible = false" />
</template>

<script lang="ts">
import { Swiper, SwiperSlide } from "swiper/vue";
import ArrowLeft from "@/assets/icons/posts/SwiperNavArrowLeft.svg?component";
import ArrowRight from "@/assets/icons/posts/SwiperNavArrowRight.svg?component";
import { repairVideoUrl } from "@/utils/embedVideoUtil";
import { defineComponent, type PropType, ref, watch } from "vue";
import ZoomModal from '@/components/tools/modal/ZoomModal.vue';
import { useSwiperconf } from "@/utils/useSwiperConf";

export default defineComponent({
    name: 'SwiperBlank',
    components: {
        Swiper,
        SwiperSlide,
        ArrowLeft,
        ArrowRight,
        ZoomModal
    },
    props: {
        images: {
            type: Array as PropType<string[]>,
            default: () => [],
        },
        videos: {
            type: Array as PropType<string[]>,
            default: () => [],
        },
        type: {
            type: String,
            default: "common",
        },
        sectionId: {
            type: Number,
        },
        activeIndexInModal: {
            type: Number
        }
    },
    setup(props) {
        const modalIsVisible = ref(false);
        const activeIndex = ref();

        watch((props), (newVal) => {
            if (newVal.activeIndexInModal && newVal.activeIndexInModal !== null || newVal.activeIndexInModal == 0) {
                activeIndex.value = newVal.activeIndexInModal;
                modalIsVisible.value = true;
            }
        }, { deep: true, immediate: true })

        const {
            swiperOn,
            slideNext,
            slidePrev,
            sliderConfig,
            swiperInstance,
            isEnd,
            isBeginning
        } = useSwiperconf(props.type);

        return {
            swiperOn,
            slideNext,
            slidePrev,
            sliderConfig,
            swiperInstance,
            isEnd,
            isBeginning,
            repairVideoUrl,
            modalIsVisible,
            activeIndex
        };
    },
})
</script>

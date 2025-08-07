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

        <!-- для встроенных video -->
        <swiper-slide v-for="(video, index) in videosEmbed"
                      :key="'postVideoEmbed' + index">
            <iframe v-if="video && video.file_url"
                    width="100%"
                    height="500px"
                    :title="'Видеоконтент'"
                    :src="String(repairVideoUrl(video?.file_url))"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
            </iframe>
        </swiper-slide>

        <!-- для загруженных video -->
        <swiper-slide v-for="(video, index) in videosNative"
                      :key="'postVideoNative' + index">
            <iframe v-if="video && video.file_url"
                    width="100%"
                    height="500px"
                    :title="'Видеоконтент'"
                    :src="String((video.file_url))"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
            </iframe>
        </swiper-slide>

    </swiper>
    <SwiperButtons :isBeginning="isBeginning"
                   :isEnd="isEnd"
                   :buttonsPos="'bottom'"
                   @slideNext="slideNext"
                   @slidePrev="slidePrev" />

    <ZoomModal v-if="modalIsVisible"
               :image="images"
               :activeIndex="activeIndex"
               @close="modalIsVisible = false" />
</template>

<script lang="ts">
import { Swiper, SwiperSlide } from "swiper/vue";
import { repairVideoUrl } from "@/utils/embedVideoUtil";
import { defineComponent, type PropType, ref, watch } from "vue";
import ZoomModal from '@/components/tools/modal/ZoomModal.vue';
import { useSwiperconf } from "@/composables/useSwiperConf";
import { type IBXFileType } from "@/interfaces/IEntities";
import SwiperButtons from "./SwiperButtons.vue";

interface ImageObject {
    file_url: string;
}

type ImageItem = string | ImageObject;
type ImageArray = ImageItem[];

export default defineComponent({
    name: 'SwiperBlank',
    components: {
        Swiper,
        SwiperSlide,
        ZoomModal,
        SwiperButtons
    },
    props: {
        images: {
            type: Array as PropType<ImageArray>,
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
        },
        videosNative: {
            type: Array<IBXFileType>
        },
        videosEmbed: {
            type: Array<IBXFileType>
        },
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

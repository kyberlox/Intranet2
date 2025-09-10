<template>
    <div class="modal__overlay modal__overlay--zoom"
         @click="close()">
        <div class="modal__overlay__close-button">
            <CloseIcon />
        </div>
        <div class="modal__wrapper modal__wrapper--zoom">
            <div class="modal__body modal__body--zoom">
                <FullWidthSlider v-if="image"
                                 :images="image"
                                 :activeIndex="activeIndex"
                                 :type="'postInner'" />
                <div v-if="video"
                     class="modal__video">
                    <iframe class="modal__video__frame"
                            :src="String(repairVideoUrl(video))"
                            title="video"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen>
                    </iframe>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { repairVideoUrl } from "@/utils/embedVideoUtil";
import { defineComponent, type PropType } from "vue";
import FullWidthSlider from "@/components/tools/swiper/FullWidthSlider.vue";
import CloseIcon from '@/assets/icons/layout/CloseIcon.svg?component';

interface ImageObject {
    file_url?: string;
}

type ImageItem = string | ImageObject;
type ImageArray = ImageItem[];

export default defineComponent({
    props: {
        image: {
            type: Array as PropType<ImageArray>,
        },
        video: {
            type: String,
        },
        activeIndex: {
            type: Number || String,
        },
    },
    components: {
        FullWidthSlider,
        CloseIcon,
    },
    setup(props, { emit }) {
        return {
            close: () => emit("close"),
            repairVideoUrl,
        };
    },
});
</script>
<template>
    <div class="modal__overlay modal__overlay--zoom"
         @click="close()">
        <div class="modal__overlay__close-button">
            <svg xmlns="http://www.w3.org/2000/svg"
                 width="30px"
                 height="30px"
                 viewBox="0 0 100 100"
                 version="1.1">

                <path style="fill:currentColor;stroke:#222222;stroke-width:4;"
                      d="M 20,4 3,21 33,50 3,80 20,97 49,67 79,97 95,80 65,50 95,20 80,4 50,34 z" />
            </svg>
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
import { type PropType } from "vue";
import FullWidthSlider from "@/components/tools/swiper/FullWidthSlider.vue";
export default {
    props: {
        image: {
            type: Array as PropType<string[]>,
        },
        video: {
            type: String,
        },
        activeIndex: {
            type: Number || String,
        }
    },
    components: {
        FullWidthSlider,
    },
    setup(props, { emit }) {
        return {
            close: () => emit("close"),
            repairVideoUrl,
        };
    },
};
</script>
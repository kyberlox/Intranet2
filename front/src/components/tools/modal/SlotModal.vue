<template>
<div @click.stop.prevent="close()"
     class="modal__overlay modal__overlay--zoom">
    <div class="modal__overlay__close-button">
        <CloseIcon />
    </div>
    <div class="modal__wrapper modal__wrapper--zoom  modal__text">
        <div class="modal__body modal__body--zoom">
            <div @click.stop.self
                 class="modal__text__content modal__text__content--points-modal">
                        <slot>
                        </slot>
            </div>
        </div>
    </div>
</div>
</template>
<script lang="ts">
import { repairVideoUrl } from "@/utils/embedVideoUtil";
import { defineComponent, type PropType } from "vue";
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
        textOnly: {
            type: Boolean,
            default: false
        },
        textContent: {
            type: Object
        },
        currentUser: {
            type: Object
        },
        modalForUserPoints: {
            type: Boolean
        }
    },
    components: {
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

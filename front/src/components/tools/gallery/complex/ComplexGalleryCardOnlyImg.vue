<template>
    <div class="flexGallery__card
                 flexGallery__card--official-events">
        <div v-for="(image, index) in slide.images"
             :key="index"
             class="flexGallery__card__img-wrapper flexGallery__card__img-wrapper--official-event">
            <img v-if="slide.images?.length"
                 @click="callModal(slide.images, index)"
                 class="flexGallery__card__img"
                 v-lazy-load="image"
                 alt="slide" />
        </div>
    </div>
</template>


<script lang="ts">
import { defineComponent, type PropType } from "vue";
import type { IUnionEntities } from "@/interfaces/IEntities";

export default defineComponent({
    name: 'ComplexGalleryCardBasic',
    props: {
        slide: {
            type: Object as PropType<IUnionEntities>,
            required: true
        },
    },
    setup(props, { emit }) {
        return {
            callModal: (slides: string[], index: number) => emit('callModal', slides, 'img', index)
        }
    }
})
</script>

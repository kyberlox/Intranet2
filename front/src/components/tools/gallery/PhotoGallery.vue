<template>
    <div class="flexGallery"
         v-if="slide">
        <div v-for="(image, index) in slide.images"
             :key="index"
             class="flexGallery__card__img-wrapper flexGallery__card__img-wrapper--official-event">
            <img v-if="slide.images"
                 @click="callModal(slide.images, index)"
                 class="flexGallery__card__img"
                 v-lazy-load="image"
                 alt="slide" />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";

interface PhotoGallerySlide {

    images?: string[]
}


export default defineComponent({
    name: 'ComplexGalleryCardOnlyImg',
    props: {
        slide: {
            type: Object as PropType<PhotoGallerySlide>
        },
    },
    setup(props, { emit }) {
        console.log('d');

        return {
            callModal: (slides: string[], index: number) => emit('callModal', slides, 'img', index)
        }
    }
})
</script>

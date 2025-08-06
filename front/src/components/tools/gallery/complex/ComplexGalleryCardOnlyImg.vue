<template>
    <div class="flexGallery__card__img-wrapper flexGallery__card__img-wrapper--official-event">
        <img @click="callModal(slide.file_url, index)"
             class="flexGallery__card__img"
             v-lazy-load="slide.file_url"
             alt="slide" />
    </div>

</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";
import type { IBXFileType } from "@/interfaces/IEntities";

interface IComplexGalleryCardOnlyImg {
    images?: string | IBXFileType
}

export default defineComponent({
    name: 'ComplexGalleryCardOnlyImg',
    props: {
        slide: {
            type: Object as PropType<IComplexGalleryCardOnlyImg>,
            required: true
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

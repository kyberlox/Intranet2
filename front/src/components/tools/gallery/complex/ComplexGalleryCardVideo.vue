<template>
    <div class="flexGallery__card flexGallery__card--official-events"
         v-for="(slide, index) in slides"
         :key="'video' + index"
         @click="callModal(slide?.indirect_data?.videoHref)">
        <div class="flexGallery__card__img-wrapper">
            <div class="flexGallery__card__img"
                 v-lazy-load="slide.indirect_data?.PREVIEW_PICTURE">
            </div>
            <PlayVideo class="flexGallery__card__play-video-icon" />
        </div>
        <div v-if="slide.name"
             class="flexGallery__card__title">{{ slide.name }}</div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { uniqueRoutesHandle } from "@/router/uniqueRoutesHandle";
import type { IUnionEntities } from "@/interfaces/IEntities";

export default defineComponent({
    name: 'ComplexGalleryCardBasic',
    props: {
        slides: {
            type: Array<IUnionEntities>,
            required: true
        },
        routeTo: {
            type: String,
            default: undefined
        },
    },
    setup(props, { emit }) {
        return {
            uniqueRoutesHandle,
            callModal: (slides: string) => emit('callModal', slides, 'video')
        }
    }
})
</script>
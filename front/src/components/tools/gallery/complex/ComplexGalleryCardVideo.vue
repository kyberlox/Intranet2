<template>
    <div class="flexGallery__card flexGallery__card--official-events">
        <div class="flexGallery__card__img-wrapper">
            <div v-if="slide.link"
                 class="flexGallery__card__img"
                 v-lazy-load="slide?.preview_file_url || slide.photo_file_url"
                 @click="callModal(slide)">
            </div>
        </div>
        <div v-if="slide.name"
             class="flexGallery__card__title">{{ slide.name }}</div>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";
import { uniqueRoutesHandle } from "@/router/uniqueRoutesHandle";
import { type IFactoryDataReports } from "@/interfaces/IEntities";


export default defineComponent({
    name: 'ComplexGalleryCardBasic',
    props: {
        slide: {
            type: Object as PropType<IFactoryDataReports>,
            required: true
        },
        routeTo: {
            type: String,
            default: undefined
        },
    },
    emits: ['callModal'],
    setup(props, { emit }) {

        return {
            uniqueRoutesHandle,
            callModal: (slide: IFactoryDataReports) => emit('callModal', slide.link, 'video')
        }
    }
})
</script>
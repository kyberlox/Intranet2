<template>
    <div class="contentGallery"
         v-if="slide">
        <div v-if=slide.images
             v-for="(image, index) in slide.images"
             :key="index"
             class="contentGallery__img-wrapper">
            <div @click="callModal(slide.images, index)"
                 class="contentGallery__card__img"
                 v-lazy-load="image.file_url"
                 alt="slide"></div>
        </div>
        <div v-if="slide.videos_embed"
             v-for="video in slide.videos_embed">
            <iframe v-if="video && video.file_url"
                    width="100%"
                    class="contentGallery__card__img"
                    height="500px"
                    :title="'Видеоконтент'"
                    :src="String(repairVideoUrl(video?.file_url))"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
            </iframe>
        </div>
        <div v-if="slide.videos_native"
             v-for="video in slide.videos_native">
            <iframe v-if="video && video.file_url"
                    width="100%"
                    class="contentGallery__card__img"
                    height="500px"
                    :title="'Видеоконтент'"
                    :src="String(repairVideoUrl(video?.file_url))"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
            </iframe>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from "vue";
import type { IBXFileType } from "@/interfaces/IEntities";
import { repairVideoUrl } from "@/utils/embedVideoUtil";

export interface IContentGallerySlide {
    name: string
    images?: IBXFileType[],
    videos_native?: IBXFileType[],
    videos_embed?: IBXFileType[]
}

export default defineComponent({
    name: 'contentGallery',
    props: {
        slide: {
            type: Object as PropType<IContentGallerySlide>
        },
    },
    setup(props, { emit }) {
        console.log(props.slide);

        return {
            callModal: (slides: IBXFileType[], index: number) => emit('callModal', slides, 'img', index),
            repairVideoUrl
        }
    }
})
</script>
<style lang="scss">
.contentGallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 25px;
    padding: 16px 0;

    @media (max-width: 768px) {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 12px;
        padding: 12px 0;
    }

    @media (max-width: 480px) {
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        padding: 8px 0;
    }

    &__card__img {
        background-image: url(http://intranet.emk.org.ru:8000/api/files/6892dd6….jpg);
        width: 100%;
        height: 100%;
        background-position: center;
        background-size: cover;
        background-repeat: no-repeat;
        cursor: zoom-in;

        &:hover {
            filter: contrast(0.7);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        }
    }

    &__img-wrapper {
        position: relative;
        aspect-ratio: 4/4;
        border-radius: 12px;
        overflow: hidden;
        background-color: #f8f9fa;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;

        background-size: contain;
    }
}
</style>
<template>
<div class="contentGallery"
     v-if="slide">
    <div v-for="(image, index) in slide.images"
         :key="index"
         class="contentGallery__img-wrapper">
        <div v-if="contest && image.indirect_data?.videos_native?.length && image.indirect_data?.videos_native[0].file_url"
             class="contentGallery__video-wrapper">
            <iframe width="100%"
                    class="contentGallery__card__video"
                    :title="'Видеоконтент'"
                    :src="String(repairVideoUrl(image.indirect_data?.videos_native[0].file_url))"
                    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    autoplay="false"
                    allowfullscreen>
            </iframe>
        </div>

        <div v-else-if="slide.images"
             @click="callModal(slide.images, index)"
             class="contentGallery__card__img"
             v-lazy-load="image.file_url || image.preview_file_url"
             alt="slide">
        </div>

        <div v-if="image.preview_file_url?.includes('mp4')"
             class="contentGallery__figure">
            <div v-if="image.indirect_data?.representative_text"
                 v-html="parseMarkdown(image.indirect_data?.representative_text)"></div>
            <div class="contentGallery__figure--category"
                 v-html="image.indirect_data?.category"></div>
        </div>

        <Reactions v-if="modifiers?.includes('likes')"
                   :reactions="(image?.reactions as IReaction)"
                   :id="Number(image.id)"
                   :type="'postPreview'"
                   :modifiers="modifiers" />

    </div>
    <div v-for="(video, index) in slide.videos_embed"
         :key="'videoEmbed' + index">
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
    <div v-for="(video, index) in slide.videos_native"
         :key="'videoNative' + index">
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
import { defineComponent, type PropType } from "vue";
import type { IBXFileType, IReaction } from "@/interfaces/IEntities";
import { repairVideoUrl } from "@/utils/embedVideoUtil";
import Reactions from "../common/Reactions.vue";
import { parseMarkdown } from "@/utils/parseMarkdown";

interface IImageItem extends IBXFileType {
    id: string;
    file_url: string;
    preview_file_url?: string;
    reactions?: IReaction;

    // для конкурсов
    indirect_data?: {
        nomination?: string,
        representative_text?: string,
        category?: string,
        videos_native?: IBXFileType[]
    }
}

export interface IContentGallerySlide {
    name?: string;
    images?: IImageItem[];
    videos_native?: IBXFileType[];
    videos_embed?: IBXFileType[];

}

export default defineComponent({
    name: 'contentGallery',
    props: {
        slide: {
            type: Object as PropType<IContentGallerySlide>
        },
        modifiers: {
            type: Array<string>
        },
        contest: {
            type: Boolean,
            default: () => false
        }
    },
    components: {
        Reactions
    },
    setup(props, { emit }) {

        return {
            callModal: (slides: IBXFileType[], index: number) => emit('callModal', index),
            repairVideoUrl,
            parseMarkdown
        }
    }
})
</script>
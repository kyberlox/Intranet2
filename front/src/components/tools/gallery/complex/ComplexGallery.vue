<template>
    <div class="flexGallery"
         v-if="slides?.length">
        <div v-for="(slide, index) in slides"
             class="flexGallery__wrapper"
             :class="{ 'hidden': routeTo == 'factoryReports' && !slide.indirect_data?.reports?.length && !slide.indirect_data?.tours?.length }"
             :key="index">
            <ComplexGalleryCardBasic :slide="slide"
                                     :modifiers="modifiers"
                                     :routeTo="routeTo" />
        </div>
        <ZoomModal :video="modalVideo"
                   :image="modalImg"
                   :activeIndex="activeIndex"
                   v-if="modalIsOpen == true"
                   @close="modalIsOpen = false" />
    </div>
    <ComplexGallerySkeleton v-else />
</template>


<script lang="ts">
import PlayVideo from "@/assets/icons/common/PlayVideo.svg?component";
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import { defineComponent, ref, type PropType } from "vue";
import { uniqueRoutesHandle } from "@/router/uniqueRoutesHandle";
import type { IFactoryDataTours, IFactoryDataReports, IBXFileType } from "@/interfaces/IEntities";
import ComplexGallerySkeleton from "./ComplexGallerySkeleton.vue";
import ComplexGalleryCardBasic from "./ComplexGalleryCardBasic.vue";

interface IComplexGallery {
    id: number,
    section_id?: number,
    indirect_data?: {
        reports?: IFactoryDataReports[],
        tours?: IFactoryDataTours[],
        videoHref?: string,
        date_from?: string,
        date_to?: string
    },
    videoHref?: string,
    link?: string,
    images?: string[],
}

export default defineComponent({
    name: 'ComplexGallery',
    props: {
        slides: {
            type: Array<IComplexGallery>,
        },
        title: {
            type: String,
        },
        modifiers: {
            type: Array<string>,
            default: () => ['']
        },
        routeTo: {
            type: String,
        },
    },
    components: {
        ZoomModal,
        ComplexGallerySkeleton,
        ComplexGalleryCardBasic,
    },
    setup(props) {
        const modalVideo = ref();
        const modalImg = ref();
        const modalIsOpen = ref(false);
        const activeIndex = ref(0);

        const callModal = (src: string[] | string, type: 'video' | 'img', imgIndex?: number) => {
            if (!src) return;
            if (type == 'video') {
                modalImg.value = '';
                modalVideo.value = src;
            }
            else if (type == 'img') {
                if (typeof imgIndex !== 'number' && !imgIndex) return;
                activeIndex.value = imgIndex;
                modalVideo.value = '';
                modalImg.value = src;
                activeIndex.value = imgIndex;
            }
            modalIsOpen.value = true;
        }

        return {
            PlayVideo,
            modalImg,
            modalVideo,
            modalIsOpen,
            activeIndex,
            callModal,
            uniqueRoutesHandle,
        }
    }
})
</script>

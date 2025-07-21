<template>
    <div class="flexGallery"
         v-if="slides?.length">
        <div v-for="(slide, index) in slides"
             class="flexGallery__wrapper"
             :key="index">
            <ComplexGalleryCardBasic v-if="checkCardType(slide) == 'basic'"
                                     :slide="slide"
                                     :modifiers="modifiers"
                                     :routeTo="routeTo"
                                     :setCardDate="setCardDate" />

            <ComplexGalleryCardOnlyImg v-else-if="checkCardType(slide) == 'onlyImg'"
                                       :slide="slide"
                                       @callModal="callModal" />

            <ComplexGalleryCardVideo v-else-if="checkCardType(slide) == 'videoCard'"
                                     :slide="slide"
                                     :routeTo="routeTo"
                                     @callModal="callModal" />
        </div>
        <ZoomModal :video="modalVideo"
                   :image="modalImg"
                   :activeIndex="activeIndex"
                   v-if="modalIsOpen == true"
                   @close="modalIsOpen = false" />
    </div>
    <RichGallerySkeleton v-else />
</template>


<script lang="ts">
import PlayVideo from "@/assets/icons/common/PlayVideo.svg?component";
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import { defineComponent, ref } from "vue";
import { getProperty } from "@/utils/getPropertyFirstPos";
import { uniqueRoutesHandle } from "@/router/uniqueRoutesHandle";
import type { IFactoryDataTours, IFactoryDataReports } from "@/interfaces/IEntities";
import RichGallerySkeleton from "./ComplexGallerySkeleton.vue";
import ComplexGalleryCardBasic from "./ComplexGalleryCardBasic.vue";
import ComplexGalleryCardOnlyImg from "./ComplexGalleryCardOnlyImg.vue";
import ComplexGalleryCardVideo from "./ComplexGalleryCardVideo.vue";

interface IComplexGallery {
    id?: number,
    section_id?: number,
    indirect_data?: {
        reports?: IFactoryDataReports[],
        tours?: IFactoryDataTours[],
        videoHref?: string,

        // Бонусы партнеров
        PROPERTY_341?: string[],
        PROPERTY_337?: string[],
        PROPERTY_338?: string[],
        PROPERTY_340?: string[],
        PROPERTY_439?: string[],
        // _______________________
        // Афиша
        PROPERTY_375?: string[],
        // ___________________________
        // Официальные события 
        PROPERTY_665?: string[],
        PROPERTY_403?: string[],
        PROPERTY_398?: string[],
        PROPERTY_399?: string[],
        PROPERTY_400?: string[],
        PROPERTY_401?: string[],
        PROPERTY_402?: string[],
        date_creation?: string
        // _______________________________
        // Корпоративная жизнь
        PROPERTY_666?: string[],
        PROPERTY_405?: string[],
        PROPERTY_406?: string[],
        PROPERTY_407?: string[],
        PROPERTY_409?: string[],
        PROPERTY_408?: string[],
        // ______________________________
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
        onlyImg: {
            type: Boolean,
            default: false
        }
    },
    components: {
        ZoomModal,
        RichGallerySkeleton,
        ComplexGalleryCardBasic,
        ComplexGalleryCardOnlyImg,
        ComplexGalleryCardVideo
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

        const setCardDate = (slide: { indirect_data?: { "PROPERTY_375"?: string[], "PROPERTY_438"?: string[] } }) => {
            return getProperty(slide, "PROPERTY_375") + ' - ' + getProperty(slide, "PROPERTY_438");
        }

        const checkCardType = (slide: IComplexGallery) => {

            if (!slide.videoHref && !props.modifiers.includes('noRoute') &&
                props.routeTo) {
                // чек на отсутствие внутренных ссылок у репортажей и 3д туров
                if (slide.section_id == 41 && (!slide?.indirect_data?.reports?.length && !slide?.indirect_data?.tours?.length)) return false;
                return 'basic';
            }
            else if (slide?.indirect_data && ('videoHref' in slide.indirect_data && slide.indirect_data.videoHref) || slide.link) {
                return 'videoCard'
            }

            else if (props.modifiers.includes('noRoute') && slide.images) {
                return 'onlyImg'
            }
        }

        return {
            PlayVideo,
            modalImg,
            modalVideo,
            callModal,
            uniqueRoutesHandle,
            modalIsOpen,
            activeIndex,
            getProperty,
            checkCardType,
            setCardDate
        }
    }
})
</script>

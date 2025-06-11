<template>
    <div class="flexGallery"
         v-if="slides?.length">
        <div v-for="(slide, index) in slides"
             :key="index">
            <RouterLink v-if="!slide.videoHref && !modifiers.includes('noRoute') && !modifiers.includes('buttons') && routeTo"
                        class="flexGallery__card"
                        :to="uniqueRoutesHandle(routeTo, slide)">
                <div class="flexGallery__card__img-wrapper"
                     :class="{ 'flexGallery__card__img-wrapper--noFullWidthImg': modifiers.includes('noFullWidthImg') }">
                    <div class="flexGallery__card__img"
                         :style="{ backgroundImage: `url(${slide.indirect_data?.PREVIEW_PICTURE ?? 'https://placehold.co/360x206'})` }">
                    </div>
                </div>
                <div v-if="slide.name"
                     class="flexGallery__card__title flexGallery__card__title--text-date">
                    <span v-if="getProperty(slide as IAfishaItem, 'PROPERTY_375')"> {{ setCardDate(slide) }}</span>
                    <span>{{ slide.name }}</span>
                </div>
            </RouterLink>

            <div v-else-if="modifiers.includes('buttons')"
                 class="flexGallery__card">
                <div class="flexGallery__card__img-wrapper"
                     :class="{ 'flexGallery__card__img-wrapper--noFullWidthImg': modifiers.includes('noFullWidthImg') }">
                    <div v-if="slide.indirect_data?.PREVIEW_PICTURE"
                         class="flexGallery__card__img"
                         :style="{ backgroundImage: `url(${slide.indirect_data?.PREVIEW_PICTURE ?? 'https://placehold.co/360x206'})` }">
                    </div>
                </div>
                <div v-if="slide.name"
                     class="flexGallery__card__title flexGallery__card__title--text-date">
                    <span v-if="getProperty(slide as IAfishaItem, 'PROPERTY_375')"> {{ setCardDate(slide) }}</span>
                    <span v-if="slide.name">{{ slide.name }}</span>
                </div>

                <div v-if="routeTo && slide.indirect_data && ('reportages' in slide.indirect_data || 'tours' in slide.indirect_data)"
                     class="flexGallery__card__buttons">
                    <RouterLink v-if="slide.indirect_data?.reportages"
                                :to="uniqueRoutesHandle(routeTo, slide, null, 'factoryReports')"
                                class="primary-button primary-button--rounder">Репортажи</RouterLink>
                    <RouterLink v-if="slide.indirect_data?.tours"
                                :to="uniqueRoutesHandle(routeTo, slide, null, 'factoryTours')"
                                class="primary-button primary-button--rounder">3D-Туры</RouterLink>
                </div>
            </div>

            <div v-else-if="modifiers.includes('noRoute') && slide.images"
                 class="flexGallery__card
                 flexGallery__card--official-events">
                <div @click="callModal(slide.images, 'img', index)"
                     class="flexGallery__card__img-wrapper flexGallery__card__img-wrapper--official-event">
                    <img class="flexGallery__card__img"
                         :src="slide.image" />
                </div>
            </div>

            <div v-else-if="slide?.indirect_data && 'videoHref' in slide.indirect_data && slide.indirect_data.videoHref"
                 class="flexGallery__card flexGallery__card--official-events"
                 v-for="(slide, index) in slides"
                 :key="'video' + index"
                 @click="callModal(slide.indirect_data.videoHref, 'video')">
                <div class="flexGallery__card__img-wrapper">
                    <div class="flexGallery__card__img"
                         :style="{ backgroundImage: `url(${slide.indirect_data?.PREVIEW_PICTURE})` }">
                    </div>
                    <PlayVideo class="flexGallery__card__play-video-icon" />
                </div>
                <div v-if="slide.name"
                     class="flexGallery__card__title">{{ slide.name }}</div>
            </div>
        </div>
        <ZoomModal :video="modalVideo"
                   :image="modalImg"
                   :activeIndex="activeIndex"
                   v-if="modalIsOpen == true"
                   @close="modalIsOpen = false" />
    </div>
    <FlexGallerySkeleton v-else />
</template>

<script lang="ts">
import PlayVideo from "@/assets/icons/common/PlayVideo.svg?component";
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import { defineComponent, ref } from "vue";
import { getProperty } from "@/utils/getPropertyFirstPos";
import { uniqueRoutesHandle } from "@/router/uniqueRoutesHandle";
import type { IAfishaItem, IUnionEntities } from "@/interfaces/IEntities";
import FlexGallerySkeleton from "./FlexGallerySkeleton.vue";

export default defineComponent({
    name: 'FlexGallery',
    props: {
        slides: {
            type: Array<IUnionEntities>,
        },
        title: {
            type: String,
        },
        modifiers: {
            type: Array,
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
        PlayVideo,
        ZoomModal,
        FlexGallerySkeleton
    },
    setup() {
        const modalVideo = ref();
        const modalImg = ref();
        const modalIsOpen = ref(false);
        const activeIndex = ref(0);

        const callModal = (src: string[], type: 'video' | 'img', imgIndex?: number) => {
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

        const setCardDate = (slide: IUnionEntities) => {
            return getProperty(slide as IAfishaItem, "PROPERTY_375") + ' - ' + getProperty(slide as IAfishaItem, "PROPERTY_438");
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
            setCardDate
        }
    }
})
</script>

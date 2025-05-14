<template>
    <div class="flexGallery"
         v-if="slides">
        <div v-for="(slide, index) in slides"
             :key="index">
            <RouterLink v-if="!slide.videoHref && !modifiers.includes('noRoute')"
                        class="flexGallery__card"
                        :to="{ name: routeTo, params: { id: slide.id } }">
                <div class="flexGallery__card__img-wrapper"
                     :class="{ 'flexGallery__card__img-wrapper--noFullWidthImg': modifiers.includes('noFullWidthImg') }">
                    <div class="flexGallery__card__img"
                         :style="{ backgroundImage: `url(${slide.img ?? 'https://placehold.co/360x206'})` }">
                    </div>
                </div>
                <div class="flexGallery__card__title flexGallery__card__title--text-date">
                    <span v-if="getProperty(slide, 'PROPERTY_375')"> {{ setCardDate(slide) }}</span>
                    <span v-if="slide.name">{{ slide.name }}</span>
                </div>
            </RouterLink>

            <div v-else-if="modifiers.includes('noRoute')"
                 class="flexGallery__card
                 flexGallery__card--official-events">

                <div @click="callModal(slides, 'img', index)"
                     class="flexGallery__card__img-wrapper flexGallery__card__img-wrapper--official-event">
                    <img class="flexGallery__card__img"
                         :src="slide.img" />
                </div>
            </div>

            <div v-else-if="slide.videoHref"
                 class="flexGallery__card flexGallery__card--official-events"
                 v-for="(slide, index) in slides"
                 :key="'video' + index"
                 @click="callModal(slide.videoHref, 'video')">
                <div class="flexGallery__card__img-wrapper">
                    <div class="flexGallery__card__img"
                         :style="{ backgroundImage: `url(${slide.img})` }">
                    </div>
                    <PlayVideo class="flexGallery__card__play-video-icon" />
                </div>
                <div class="flexGallery__card__title">{{ slide.name }}</div>
            </div>
        </div>
        <ZoomModal :video="modalVideo"
                   :image="modalImg"
                   :activeIndex="activeIndex"
                   v-if="modalIsOpen == true"
                   @close="modalIsOpen = false" />
    </div>


</template>

<script lang="ts">
import PlayVideo from "@/assets/icons/common/PlayVideo.svg?component";
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import { defineComponent, ref } from "vue";
import type { RouteLocationRaw } from 'vue-router';
import type { IAfishaItem } from "@/interfaces/IEntities";
import { getProperty } from "@/utils/fieldChecker";

export default defineComponent({
    name: 'FlexGallery',
    props: {
        slides: {
            type: Array<IAfishaItem>,
        },
        title: {
            type: String,
        },
        page: {
            type: String,
        },
        modifiers: {
            type: Array,
            default: () => ['']
        },
        routeTo: {
            type: String,
            required: true,
        },
        onlyImg: {
            type: Boolean,
            default: false
        }
    },
    components: {
        PlayVideo,
        ZoomModal
    },
    setup(props) {
        const modalVideo = ref();
        const modalImg = ref();
        const modalIsOpen = ref(false);
        const activeIndex = ref(0);

        const callModal = (src: string, type: 'video' | 'img', imgIndex?: number) => {
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

        const checkRouteTo = (slide): RouteLocationRaw => {
            if (props.page === 'experience') {
                return { name: 'experienceTypes', params: { title: slide.href } }
            }
            else if (props.page === 'experienceTypes') {
                return { name: 'experienceType', params: { title: props.title, id: slide.id } }
            }
            else if (props.page === 'tours') {
                return { name: 'factoryTour', params: { title: slide.hrefTitle, id: slide.hrefId } }
            } else if (props.page === 'officialEvents') {
                return { name: 'officialEvent', params: { id: slide.href } };
            }
            else return '/';
        }

        const setCardDate = (slide) => {
            return getProperty(slide, "PROPERTY_375") + ' - ' + getProperty(slide, "PROPERTY_438");
        }

        return {
            PlayVideo,
            modalImg,
            modalVideo,
            callModal,
            checkRouteTo,
            modalIsOpen,
            activeIndex,
            getProperty,
            setCardDate
        }
    }
})
</script>

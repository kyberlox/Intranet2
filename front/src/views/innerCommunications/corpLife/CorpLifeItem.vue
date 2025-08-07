<template>
    <div class="experience__page mt20">
        <div class="page__title">Корпоративная жизнь</div>
        <div class="page__title__details"
             v-if="title">{{ title }}</div>
        <ContentGallery v-if="formattedSlides"
                        class="mt20"
                        :page=page
                        :modifiers="modifiers"
                        :slide="slide"
                        @callModal="callModal" />
    </div>
    <ZoomModal v-if="slide && slide.images?.length && modalIsOpen == true"
               :activeIndex="activeIndex"
               :image="slide.images"
               @close="modalIsOpen = false" />
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import ContentGallery from "@/components/tools/gallery/ContentGallery.vue";
import Api from "@/utils/Api";
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import type { IContentGallerySlide } from "@/components/tools/gallery/ContentGallery.vue";

export default defineComponent({
    components: {
        ContentGallery,
        ZoomModal
    },
    props: {
        id: {
            type: String,
            required: true
        }
    },
    setup(props) {
        const slide = ref<IContentGallerySlide>();
        const formattedSlides = ref({ images: [], id: '', videos_embed: [], videos_native: [] });
        const activeIndex = ref<number>();
        const modalIsOpen = ref<boolean>();

        const callModal = (a = null, b = null, index: number, d = null) => {
            activeIndex.value = index;
            modalIsOpen.value = true;
        }

        onMounted(() => {
            Api.get(`article/find_by_ID/${props.id}`)
                .then((data) => {
                    slide.value = data;
                    formattedSlides.value.images = data.images;
                    formattedSlides.value.videos_embed = data.videos_embed;
                    formattedSlides.value.videos_native = data.videos_native;
                    formattedSlides.value.id = data.id
                })
        })

        return {
            title: slide.value?.name,
            formattedSlides,
            page: 'officialEvent',
            modifiers: ['noRoute'],
            slide,
            activeIndex,
            modalIsOpen,
            callModal
        };
    },
});
</script>

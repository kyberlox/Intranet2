<template>
    <div class="experience__page mt20">
        <div class="page__title">Корпоративная жизнь</div>
        <div class="page__title__details"
             v-if="title">{{ title }}</div>
        <PhotoGallery v-if="formattedSlides"
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
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { defineComponent, type Ref, ref, onMounted } from "vue";
import PhotoGallery from "@/components/tools/gallery/ContentGallery.vue";
import Api from "@/utils/Api";
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import { type IBXFileType } from "@/interfaces/IEntities";

interface PhotoGallerySlide {
    name: string,
    images?: IBXFileType[],
    videos_native?: IBXFileType[],
    videos_embed?: IBXFileType[]
}

export default defineComponent({
    components: {
        ComplexGallery,
        PhotoGallery,
        ZoomModal
    },
    props: {
        id: {
            type: String,
            required: true
        }
    },
    setup(props) {
        const slide: Ref<PhotoGallerySlide | undefined> = ref();
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

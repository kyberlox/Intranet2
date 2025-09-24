<template>
<div class="contest__page mt20">
    <div class="page__title">Конкурсы ЭМК</div>
    <div class="page__title__details"
         v-if="title">
        {{ title }}
    </div>
    <ContentGallery v-if="slides && slides.images?.length"
                    class="mt20"
                    :slide="slides"
                    :modifiers="['likes']"
                    @callModal="callModal" />
    <div v-else>
        <h5>Сейчас нет актуальных конкурсов</h5>
    </div>
</div>
<ZoomModal v-if="slides && slides.images?.length && modalIsOpen == true"
           :activeIndex="activeIndex"
           :image="slides.images"
           @close="modalIsOpen = false" />
</template>

<script lang="ts">
import { sectionTips } from '@/assets/static/sectionTips';
import Api from '@/utils/Api';
import { onMounted, defineComponent, ref } from 'vue';
import ContentGallery from '@/components/tools/gallery/ContentGallery.vue';
import ZoomModal from '@/components/tools/modal/ZoomModal.vue';
import { type IContentGallerySlide } from '@/components/tools/gallery/ContentGallery.vue';
import firstPlaceMedal from '@/assets/imgs/1placeMedal.png'
import secondPlaceMedal from '@/assets/imgs/2placeMedal.png'
import thirdPlaceMedal from '@/assets/imgs/3placeMedal.png'


export default defineComponent({
    components: {
        ContentGallery,
        ZoomModal
    },
    setup() {
        const slides = ref<IContentGallerySlide>();
        const title = ref();
        const modalIsOpen = ref(false);
        const activeIndex = ref();

        const callModal = (param1: undefined, param2: undefined, id: number) => {
            activeIndex.value = id;
            modalIsOpen.value = true;
        }

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Конкурсы']}`)
                .then((data) => {
                    slides.value!.images = data;
                })
        })

        return {
            slides,
            title,
            modalIsOpen,
            callModal,
            activeIndex
        };
    },
});
</script>
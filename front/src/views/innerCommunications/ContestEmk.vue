<template>
<div class="contest__page mt20">
    <div class="page__title">Конкурсы ЭМК</div>
    <div class="page__title__details"
         v-if="title">
        {{ title }}
    </div>
    <div class="tags">
        <div class="tag__wrapper"
             v-for="(nav, index) in navigation"
             :key="index">
            <div @click="pickSection(nav)"
                 :class="['tags__tag section__item__link btn-air', { 'tags__tag--active': activeNav == nav }]">
                {{ nav }}
            </div>
        </div>
    </div>
    <ContentGallery v-if="slides && slides.images?.length"
                    :key="`gallery-${activeNav}-${slides?.images?.length || 0}`"
                    class="mt20"
                    :slide="{ images: slides.images.filter((e) => e.indirect_data!.nomination == activeNav) }"
                    :modifiers="['likes', 'noViews']"
                    :contest="true"
                    @callModal="callModal" />
    <div v-else-if="!isLoading">
        <h5>Сейчас нет актуальных конкурсов</h5>
    </div>
    <div class="contest__page__loader__wrapper"
         v-else-if="isLoading">
        <Loader class="contest__page__loader" />
    </div>
</div>
<ZoomModal v-if="slides && slides.images?.length && modalIsOpen == true"
           :activeIndex="activeIndex"
           :image="slides.images.filter((e) => e.indirect_data!.nomination == activeNav)"
           @close="modalIsOpen = false" />
</template>

<script lang="ts">
import { sectionTips } from '@/assets/static/sectionTips';
import Api from '@/utils/Api';
import { onMounted, defineComponent, ref } from 'vue';
import ContentGallery from '@/components/tools/gallery/ContentGallery.vue';
import ZoomModal from '@/components/tools/modal/ZoomModal.vue';
import { type IContentGallerySlide } from '@/components/tools/gallery/ContentGallery.vue';
// import firstPlaceMedal from '@/assets/imgs/1placeMedal.png'
// import secondPlaceMedal from '@/assets/imgs/2placeMedal.png'
// import thirdPlaceMedal from '@/assets/imgs/3placeMedal.png'
import type { IContest } from '@/interfaces/entities/IContest';
import Loader from '@/components/layout/Loader.vue';

export default defineComponent({
    components: {
        ContentGallery,
        ZoomModal,
        Loader
    },
    setup() {
        const slides = ref<IContentGallerySlide>({ name: '', images: [] });
        const title = ref();
        const modalIsOpen = ref(false);
        const activeIndex = ref();
        const navigation = ref<string[]>([]);
        const isLoading = ref(true);
        const activeNav = ref();

        const callModal = (id: number) => {
            activeIndex.value = id;
            modalIsOpen.value = true;
        }

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Конкурсы']}`)
                .then((data) => {
                    slides.value.images = data.filter((e: IContest) => e.indirect_data.nomination);
                    if (!slides.value.images) return
                    slides.value.images.map((e) => {
                        const target = e.indirect_data?.nomination;
                        if (!target || navigation.value.find((e) => e == target)) return
                        navigation.value.push(target)
                        activeNav.value = navigation.value[0]
                    })
                })
                .finally(() => isLoading.value = false)
        })

        const pickSection = (nav: string) => {
            activeNav.value = nav;
        }

        return {
            slides,
            title,
            modalIsOpen,
            navigation,
            activeIndex,
            isLoading,
            activeNav,
            callModal,
            pickSection
        };
    },
});
</script>
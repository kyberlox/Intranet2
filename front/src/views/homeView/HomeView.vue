<template>
<div class="homeview mt20">
    <div v-if="mainPageCards.length"
         class="homeview__grid">
        <div v-for="item in mainPageCards"
             :class="[{ 'homeview__grid__card--fullRowBlock': item.type == 'fullRowBlock' }, { 'homeview__grid__card--singleBlock': item.type == 'swiper' }]"
             :key="item.id">
            <!-- Для слайдеров в одну ячейку -->
            <MainPageSoloBlock v-if="item.type == 'swiper'"
                               :card="item" />

            <!-- Для отдельных постов в одну строку -->
            <div class="homeview__grid"
                 v-else-if="item.type == 'fullRowBlock'">

                <MainPageRowBlocks v-for="(block, index) in item.images"
                                   :card="block"
                                   :href="item.href"
                                   :key="index + 'fullrowblock'">
                    <RouterLink :to="{ name: item.sectionId }"
                                class="homeview__grid__card__group-title">
                        {{ item.title }}
                    </RouterLink>
                </MainPageRowBlocks>

            </div>
        </div>
    </div>
    <SampleGallerySkeleton v-else />
</div>
</template>

<script lang="ts">
import { computed, defineComponent, onBeforeMount, type ComputedRef } from "vue";
import MainPageSoloBlock from "./components/MainPageSoloBlock.vue";
import MainPageRowBlocks from "./components/MainPageRowBlocks.vue";
import type { MainPageCards } from "@/interfaces/IMainPage";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import { watch } from "vue";
import { useLoadingStore } from "@/stores/loadingStore";
import SampleGallerySkeleton from "@/components/tools/gallery/sample/SampleGallerySkeleton.vue";
import { homeslug } from "@/assets/static/home";
export default defineComponent({
    name: "main-page",
    components: {
        MainPageSoloBlock,
        MainPageRowBlocks,
        SampleGallerySkeleton
    },
    setup() {
        const useViewsData = useViewsDataStore();
        const loadingStore = useLoadingStore();

        const mainPageCards: ComputedRef<MainPageCards> = computed(() => {
            const data = useViewsData.getData('homeData') as MainPageCards;
            return Array.isArray(data) ? data : [];
        });

        onBeforeMount(() => {
            if (mainPageCards.value.length) return;
            // loadingStore.setLoadingStatus(true);
            // Api.get(`article/find_by/${sectionTips['Главная']}`)
            //     .then((data: MainPageCards) => {
            //         const result = data;
            //         if (!result) return;
            //         result.find(item => item.type == 'mixedRowBlock')?.content.map((item) => {
            //             if (item.type == 'fullRowBlock' && item.images.length > 4) {
            //                 item.images.length = 4
            //             }
            //         });
            //         useViewsData.setData(result, 'homeData');
            //     })
            useViewsData.setData(homeslug, 'homeData');
        })

        watch(mainPageCards, (newVal) => {
            if (newVal && newVal.length) {
                loadingStore.setLoadingStatus(false);
            }
        }, { immediate: true, deep: true })

        return {
            mainPageCards
        };
    },
});
</script>
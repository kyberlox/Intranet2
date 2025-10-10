<template>
<div class="homeview mt20">
    <div v-if="mainPageCards.length"
         class="homeview__grid">
        <div v-for="item in mainPageCards.filter((e) => !(e.title == 'Афиша' && e.images.length == 0))"
             :class="[{ 'homeview__grid__card--section': item.type == 'section' }, { 'homeview__grid__card--swiper': item.type == 'swiper', 'homeview__grid__card--swiper--afisha': item.title == 'Афиша' }]"
             :key="item.id">
            <!-- Для слайдеров в одну ячейку -->
            <HomeViewSwiperBlock v-if="item.type == 'swiper'"
                                 :card="item" />
            <!-- Для отдельных постов в одну строку -->
            <div class="homeview__grid homeview__grid__rows"
                 v-else-if="item.type == 'section'">
                <HomeViewSectionBlock v-for="(block, index) in item.images"
                                      :card="block"
                                      :href="item.href"
                                      :key="index + 'section'">
                    <RouterLink :to="{ name: item.sectionId }"
                                class="homeview__grid__card__group-title">
                        {{ item.title }}
                    </RouterLink>
                </HomeViewSectionBlock>
            </div>
        </div>
    </div>
    <SampleGallerySkeleton v-else />
</div>
</template>

<script lang="ts">
import { computed, defineComponent, onBeforeMount, type ComputedRef } from "vue";
import HomeViewSwiperBlock from "./components/HomeViewSwiperBlock.vue";
import HomeViewSectionBlock from "./components/HomeViewSectionBlock.vue";
import type { MainPageCards } from "@/interfaces/IMainPage";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import SampleGallerySkeleton from "@/components/tools/gallery/sample/SampleGallerySkeleton.vue";

export default defineComponent({
    name: "main-page",
    components: {
        HomeViewSwiperBlock,
        HomeViewSectionBlock,
        SampleGallerySkeleton
    },
    setup() {
        const useViewsData = useViewsDataStore();
        const mainPageCards: ComputedRef<MainPageCards> = computed(() => {
            const data = useViewsData.getData('homeData') as MainPageCards;
            return Array.isArray(data) ? data : [];
        });
        onBeforeMount(() => {
            if (mainPageCards.value.length) return;
            Api.get(`article/find_by/${sectionTips['Главная']}`)
                .then((data: MainPageCards) => {
                    const result = data;
                    if (!result) return;

                    useViewsData.setData(result, 'homeData');
                })
        })

        return {
            mainPageCards
        };
    },
});
</script>
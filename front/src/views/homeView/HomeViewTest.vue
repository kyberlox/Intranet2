<template><!-- Единый контейнер с явными правилами -->
<div class="homeview">
    <!-- Single Blocks - первый ряд -->
    <div class="homeview__grid homeview__grid--solo">
        <div v-for="item in soloBlock"
             :key="item.id"
             class="homeview__item">
            {{ item.title }}
        </div>
    </div>

    <!-- Full Row Blocks -->
    <div v-for="item in rowBlock"
         :key="item.id"
         class="homeview__grid homeview__grid--full">
        <h2 class="homeview__title">{{ item.title }}</h2>
        <div class="homeview__grid-inner">
            <div v-for="image in item.images"
                 :key="image.id"
                 class="homeview__item homeview__item--full">
                {{ image.title }}
            </div>
        </div>
    </div>

    <!-- Mixed Blocks -->
    <div v-for="item in mixedBlock"
         :key="item.id"
         class="homeview__grid homeview__grid--mixed">
        <div v-for="contentItem in item.content"
             :key="contentItem.id || contentItem.title"
             :class="{
                'homeview__mixed-single': contentItem.type === 'singleBlock',
                'homeview__mixed-full': contentItem.type === 'fullRowBlock'
            }">
            <div v-if="contentItem.type === 'singleBlock'">
                {{ contentItem.title }}
            </div>
            <div v-else-if="contentItem.type === 'fullRowBlock'">
                <h3>{{ contentItem.title }}</h3>
                <div class="homeview__grid-inner">
                    <div v-for="image in contentItem.images"
                         :key="image.id"
                         class="homeview__item">
                        {{ image.title }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped>
.homeview {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

/* Базовый грид */
.homeview__grid {
    display: grid;
    gap: 1rem;
}

/* Single blocks - всегда 5 колонок */
.homeview__grid--solo {
    grid-template-columns: repeat(5, 1fr);
}

/* Full row blocks - тоже 5 колонок */
.homeview__grid--full {
    grid-template-columns: 1fr;
}

.homeview__grid-inner {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
}

/* Mixed blocks - 2 колонки (single + full) */
.homeview__grid--mixed {
    grid-template-columns: 1fr 2fr;
    gap: 2rem;
}

.homeview__mixed-full .homeview__grid-inner {
    grid-template-columns: repeat(4, 1fr);
    /* или 5, в зависимости от дизайна */
}

/* Общие стили для элементов */
.homeview__item {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    min-height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.homeview__title {
    margin-bottom: 1rem;
}

/* Адаптивность */
@media (max-width: 1200px) {

    .homeview__grid--solo,
    .homeview__grid-inner {
        grid-template-columns: repeat(4, 1fr);
    }
}

@media (max-width: 992px) {

    .homeview__grid--solo,
    .homeview__grid-inner {
        grid-template-columns: repeat(3, 1fr);
    }

    .homeview__grid--mixed {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {

    .homeview__grid--solo,
    .homeview__grid-inner {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 576px) {

    .homeview__grid--solo,
    .homeview__grid-inner {
        grid-template-columns: 1fr;
    }
}
</style>

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
            loadingStore.setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Главная']}`)
                .then((data: MainPageCards) => {
                    const result = data;
                    if (!result) return;
                    result.find(item => item.type == 'mixedRowBlock')?.content.map((item) => {
                        if (item.type == 'fullRowBlock' && item.images.length > 4) {
                            item.images.length = 4
                        }
                    });
                    useViewsData.setData(result, 'homeData');
                })
        })

        watch(mainPageCards, (newVal) => {
            if (newVal && newVal.length) {
                loadingStore.setLoadingStatus(false);
            }
        }, { immediate: true, deep: true })

        return {
            mainPageCards,
            soloBlock: computed(() => mainPageCards.value.filter((e) => e.type == 'singleBlock')),
            rowBlock: computed(() => mainPageCards.value.filter((e) => e.type == 'fullRowBlock')),
            mixedBlock: computed(() => mainPageCards.value.filter((e) => e.type == 'mixedRowBlock')),
        };
    },
});
</script>
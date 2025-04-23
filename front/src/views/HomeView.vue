<template>
    <div class="home__view mt20">
        <div class="home__view__grid">
            <div v-for="item in mainPageCards"
                 class="home__view__grid__card d-flex flex-column"
                 :class="{ 'home__view__grid__card--fullRowBlock': item.type == 'fullRowBlock' || item.type == 'mixedRowBlock' }"
                 :key="item.id">
                <!-- Для слайдеров в одну ячейку -->
                <MainPageSoloBlock v-if="item.type == 'singleBlock'"
                                   :card="item" />

                <!-- Для отдельных постов в одну строку -->
                <div v-else-if="item.type == 'fullRowBlock'"
                     class="home__view__grid__cards--fullRowBlock">
                    <span class="home__view__grid__card__group-title">{{ item.title }}</span>
                    <div class="home__view__grid">
                        <MainPageRowBlocks v-for="(block, index) in item.images"
                                           :card="block"
                                           :key="index + 'fullrowblock'" />
                    </div>
                </div>

                <!-- Все вместе -->
                <div class="home__view__grid"
                     v-else-if="item.type == 'mixedRowBlock'">
                    <div v-for="(block, index) in item.content"
                         :key="index"
                         :class="{ 'grid-span-4': block.type == 'fullRowBlock' }">
                        <MainPageSoloBlock v-if="block.type == 'singleBlock'"
                                           :card="block" />
                        <div class="home__view__grid home__view__grid--mixed"
                             v-else-if="block.type == 'fullRowBlock'">
                            <MainPageRowBlocks v-for="(blockSlides, index) in block.images"
                                               :card="typeof blockSlides === 'string' ? { id: item.id, image: blockSlides } : blockSlides"
                                               :key="index + 'fullrowblock'"
                                               :blockTitle="'Корпоративные события'"
                                               :modifiers="['mixedType']" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { mainPageCards } from "@/assets/staticJsons/mainPage";
import MainPageSoloBlock from "@/components/homePage/MainPageSoloBlock.vue";
import MainPageRowBlocks from "@/components/homePage/MainPageRowBlocks.vue";

export default defineComponent({
    name: "main-page",
    components: {
        MainPageSoloBlock,
        MainPageRowBlocks
    },
    setup() {
        mainPageCards.find(item => item.type == 'mixedRowBlock')?.content.map((item) => {
            if (item.type == 'fullRowBlock' && item.images.length > 4) {
                item.images.length = 4
            }
        });

        return {
            mainPageCards
        };
    },
});
</script>

<style>
.grid-span-4 {
    grid-column: span 4;
}

/* .home__view__grid__card__link>.home__view__grid__card__group-title:empty:not(home__view__grid__card__group-title--mixed:empty) {
    display: block;
    visibility: hidden;
} */

.home__view__grid__card__group-title--mixed {
    display: -webkit-box;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1;
    min-height: 2em;
    color: var(--emk-brand-color);
    font-weight: 600;
    font-size: 18px;
    line-height: 24px;
    /* height: 30px; */
    text-wrap-mode: nowrap;
    text-wrap-mode: wrap;
    padding-bottom: 5px;
}

.home__view__grid__card__group-title--mixed:empty {
    /* display: none;xxxx */
}
</style>
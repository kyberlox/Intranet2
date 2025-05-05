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
import { defineComponent, onMounted, ref, type Ref } from "vue";
import MainPageSoloBlock from "@/components/homePage/MainPageSoloBlock.vue";
import MainPageRowBlocks from "@/components/homePage/MainPageRowBlocks.vue";
import Api from "@/utils/Api";
import type { MainPageCards } from "@/interfaces/IMainPage";
import { sectionTips } from "@/assets/staticJsons/sectionTips";

export default defineComponent({
    name: "main-page",
    components: {
        MainPageSoloBlock,
        MainPageRowBlocks
    },
    setup() {
        const mainPageCards: Ref<MainPageCards | undefined> = ref();
        onMounted(() => {
            Api.get(`section/${sectionTips['Главная']}`)
                .then((data) => {
                    mainPageCards.value = data
                })
                .then(() => {
                    if (!mainPageCards.value) return;
                    mainPageCards.value.find(item => item.type == 'mixedRowBlock')?.content.map((item) => {
                        if (item.type == 'fullRowBlock' && item.images.length > 4) {
                            item.images.length = 4
                        }
                    });
                })
        })

        return {
            mainPageCards
        };
    },
});
</script>
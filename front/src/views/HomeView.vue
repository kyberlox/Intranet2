<template>
    <div class="homeview mt20">
        <div class="homeview__grid">
            <div v-for="item in mainPageCards"
                 class="homeview__grid__card d-flex flex-column"
                 :class="{ 'homeview__grid__card--fullRowBlock': item.type == 'fullRowBlock' || item.type == 'mixedRowBlock' }"
                 :key="item.id">
                <!-- Для слайдеров в одну ячейку -->
                <MainPageSoloBlock v-if="item.type == 'singleBlock'"
                                   :card="item" />

                <!-- Для отдельных постов в одну строку -->
                <div v-else-if="item.type == 'fullRowBlock'"
                     class="homeview__grid__cards--fullRowBlock">
                    <span class="homeview__grid__card__group-title">{{ item.title }}</span>
                    <div class="homeview__grid">
                        <MainPageRowBlocks v-for="(block, index) in item.images"
                                           :card="block"
                                           :key="index + 'fullrowblock'" />
                    </div>
                </div>

                <!-- Все вместе -->
                <div class="homeview__grid"
                     v-else-if="item.type == 'mixedRowBlock'">
                    <div v-for="(block, index) in item.content"
                         :key="index"
                         :class="{ 'grid-span-4': block.type == 'fullRowBlock' }">
                        <MainPageSoloBlock v-if="block.type == 'singleBlock'"
                                           :card="block" />
                        <div class="homeview__grid homeview__grid--mixed"
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
import { computed, defineComponent, onMounted, ref, type Ref } from "vue";
import MainPageSoloBlock from "@/components/homePage/MainPageSoloBlock.vue";
import MainPageRowBlocks from "@/components/homePage/MainPageRowBlocks.vue";
import Api from "@/utils/Api";
import type { MainPageCards } from "@/interfaces/IMainPage";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import { watch } from "vue";
import { useLoadingStore } from "@/stores/loadingStore"

export default defineComponent({
    name: "main-page",
    components: {
        MainPageSoloBlock,
        MainPageRowBlocks
    },
    setup(props, { emit }) {
        const useViewsData = useViewsDataStore();
        const loadingStore = useLoadingStore();
        // const mainPageCards: Ref<MainPageCards | undefined> = ref();
        const mainPageCards = computed(() => useViewsData.getData('homeData'))
        onMounted(() => {
            if (mainPageCards.value.length) return;
            loadingStore.setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Главная']}`)
                .then((data) => {
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
            mainPageCards
        };
    },
});
</script>
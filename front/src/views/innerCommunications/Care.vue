<template>
    <div class="page__title mt20">Благотворительные проекты</div>
    <div v-if="careSlides.length"
         class="care__section">
        <div v-for="(item, index) in careSlides"
             :key="'safe' + index"
             class="safetyTechnics__card">
            <VerticalCard :card="item"
                          :page="'care'"
                          :modifiers="['needLogo']"
                          :routeTo='"carePost"' />
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, onMounted, computed, type ComputedRef } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import type { ICareSlide } from "@/interfaces/IEntities";
import { useViewsDataStore } from "@/stores/viewsData";
import VerticalCard from "@/components/tools/common/VerticalCard.vue";


export default defineComponent({
    components: {
        VerticalCard,
    },
    setup() {
        const careSlides: ComputedRef<ICareSlide[]> = computed(() => useViewsDataStore().getData('careData') as ICareSlide[]);

        onMounted(() => {
            if (careSlides.value.length) return;
            Api.get(`article/find_by/${sectionTips['Благотворительность']}`)
                .then((res) => {
                    useViewsDataStore().setData(res, "careData")
                })
        })

        return {
            careSlides,
        };
    },
});
</script>

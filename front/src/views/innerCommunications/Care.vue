<template>
    <div class="page__title mt20">Благотворительные проекты</div>
    <div class="d-flex flex-column">
        <div class="section__image__list__section order-1 order-md-2">
            <div class="section__image__list__items row">
                <SafetyTechnicsSlide v-for="slide in careSlides"
                                     :key="slide.id"
                                     :slide="slide"
                                     :routeTo="'carePost'"
                                     :modifiers="['noCenterTitle']" />
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import SafetyTechnicsSlide from "@/views/about/safetyTechnics/components/SafetyTechnicsSlide.vue";
import { defineComponent, onMounted, computed, type ComputedRef } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import type { ICareSlide } from "@/interfaces/IEntities";
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from "@/stores/loadingStore";

export default defineComponent({
    components: {
        SafetyTechnicsSlide,
    },
    setup() {
        const careSlides: ComputedRef<ICareSlide[]> = computed(() => useViewsDataStore().getData('careData') as ICareSlide[]);
        onMounted(() => {
            if (careSlides.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Благотворительность']}`)
                .then((res) => {
                    useViewsDataStore().setData(res, "careData")
                })
                .finally(() => {
                    useLoadingStore().setLoadingStatus(false);
                })
        })
        return {
            careSlides,
        };
    },
});
</script>

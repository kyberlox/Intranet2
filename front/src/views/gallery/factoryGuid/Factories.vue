<template>
    <div class="experience__page mt20">
        <div class="page__title">Гид по предприятиям </div>
        <ComplexGallery :slides="factoriesSlides"
                        :modifiers="['noFullWidthImg', 'buttons']"
                        :routeTo="'experienceTypes'" />
    </div>
</template>

<script lang="ts">
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { defineComponent, computed, type ComputedRef } from "vue";
import type { IFactoryGuidSlides } from "@/interfaces/IEntities";
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";

export default defineComponent({
    components: {
        ComplexGallery,
    },
    setup() {
        const factoryGuidData = useFactoryGuidDataStore();
        const factoriesSlides: ComputedRef<IFactoryGuidSlides[]> = computed(() => factoryGuidData.getAllFactories as IFactoryGuidSlides[]);
        return {
            factoriesSlides,
        };
    },
});
</script>

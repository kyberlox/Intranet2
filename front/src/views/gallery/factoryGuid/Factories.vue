<template>
    <div class="experience__page mt20">
        <div class="page__title">Гид по предприятиям </div>
        <ComplexGallery :slides="factoriesSlides"
                        :modifiers="['noFullWidthImg', 'buttons']"
                        :routeTo="'experienceTypes'" />
    </div>
</template>

<script lang="ts">
import { sectionTips } from "@/assets/static/sectionTips";
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import Api from "@/utils/Api";
import { defineComponent, onMounted, computed, type ComputedRef } from "vue";
import type { IFactoryGuidSlides } from "@/interfaces/IEntities";
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";

export default defineComponent({
    components: {
        ComplexGallery,
    },
    setup() {
        const factoryGuidData = useFactoryGuidDataStore();
        const factoriesSlides: ComputedRef<IFactoryGuidSlides[]> = computed(() => factoryGuidData.getAllFactories as IFactoryGuidSlides[]);
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['гидПредприятия']}`)
                .then((data) => {
                    factoryGuidData.setAllFactories(data)
                })
        })
        return {
            factoriesSlides,
        };
    },
});
</script>

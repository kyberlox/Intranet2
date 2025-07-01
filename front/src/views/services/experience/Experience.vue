<template>
    <div class="experience__page mt20">
        <div class="page__title">Референсы и опыт поставок</div>
        <ComplexGallery :page="page"
                        :slides="slides"
                        :modifiers="['noFullWidthImg']"
                        :routeTo="'experienceTypes'" />
    </div>
</template>

<script lang="ts">
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { defineComponent, onMounted, ref, type Ref, watch } from "vue";
import { useExperienceData } from "@/utils/useExperienceData";

export default defineComponent({
    components: {
        ComplexGallery,
    },
    setup() {
        const slides: Ref<{
            factoryId: number;
            slides: string[];
            name: string;
        }[]> = ref([]);

        const { loadExperienceData, generateSlides } = useExperienceData();

        const initializeData = () => {
            const data = loadExperienceData();

            watch(data, (newValue) => {
                if (Object.keys(newValue).length) {
                    slides.value = generateSlides(newValue);
                }
            }, { deep: true, immediate: true });
        };

        onMounted(() => {
            initializeData();
        });

        return {
            slides,
            page: "experience",
        };
    }
});
</script>

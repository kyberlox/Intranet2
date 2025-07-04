<template>
    <div class="experience__page mt20">
        <div class="page__title">Референсы и опыт поставок</div>
        <ComplexGallery :page="page"
                        :slides="slides"
                        :title="typeof title == 'string' ? title : ''"
                        :modifiers="['noFullWidthImg']"
                        :routeTo="'experienceType'" />
    </div>
</template>

<script lang="ts">
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { useRoute } from "vue-router";
import { defineComponent, onMounted, ref, type Ref, watch } from "vue";
import { useExperienceData } from "@/utils/useExperienceData";
import { useReferencesAndExpDataStore } from "@/stores/ReferencesAndExpData";
import { sectorLogoTips } from "../../../assets/static/factoryLogoTips";
import type { IDocument } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        ComplexGallery,
    },
    props: {
        factoryId: { type: String, required: true }
    },
    setup(props) {
        const route = useRoute();
        const title = ref(route.params.title);
        const slides: Ref<{ id: number, factoryId: number, sectorId: string, name: string, attach: IDocument[], preview_file_url: string }[]> = ref([]);

        const { loadExperienceData } = useExperienceData();

        const getLogo = (sectorId: keyof typeof sectorLogoTips) => {
            return sectorLogoTips[sectorId];
        }


        const initializeData = () => {
            const data = loadExperienceData();
            watch(data, (newValue) => {
                if (Object.keys(newValue).length && props.factoryId) {
                    const currentContent = useReferencesAndExpDataStore().getCurrentFactory(props.factoryId);

                    slides.value = currentContent.sectors.map((sector) => ({
                        id: Number(props.factoryId),
                        factoryId: Number(props.factoryId),
                        sectorId: sector.sectorId,
                        name: sector.sectorTitle,
                        attach: sector.sectorDocs ?? [],
                        preview_file_url: getLogo(sector.sectorId as keyof typeof sectorLogoTips)
                    }));
                    console.log(slides.value);

                }
            }, { deep: true, immediate: true });
        };

        onMounted(() => {
            initializeData();
        });

        return {
            slides,
            page: "experienceTypes",
            title,
        };
    },
});
</script>

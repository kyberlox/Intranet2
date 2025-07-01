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
import { defineComponent, onMounted, ref, type Ref, computed, watch } from "vue";
import { useExperienceData } from "@/utils/useExperienceData";
import { useReferencesAndExpDataStore } from "@/stores/ReferencesAndExpData";
import { sectorLogoTips } from "../../../assets/static/factoryLogoTips";

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
        const slides: Ref<{ factoryId: number, slides: string[], name: string }[]> = ref([]);

        const { loadExperienceData } = useExperienceData();

        const getLogo = (sectorId: string) => {
            console.log(sectorId);

            return sectorLogoTips[sectorId];
        }


        const initializeData = () => {
            const data = loadExperienceData();
            watch(data, (newValue) => {
                if (Object.keys(newValue).length && props.factoryId) {
                    const currentContent = useReferencesAndExpDataStore().getCurrentFactory(props.factoryId);

                    slides.value = currentContent.sectors.map((sector) => ({
                        factoryId: Number(props.factoryId),
                        sectorId: sector.sectorId,
                        name: sector.sectorTitle,
                        attach: sector.sectorDocs,
                        preview_file_url: getLogo(sector.sectorId)
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

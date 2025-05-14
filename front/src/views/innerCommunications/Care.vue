<template>
    <div class="page__title mt20">Благотворительные проекты</div>
    <div class="d-flex flex-column">
        <div class="section__image__list__section order-1 order-md-2">
            <div class="section__image__list__items row">
                <SafetyTechnicsSlide v-for="slide in careSlides"
                                     :key="slide.id"
                                     :slide="slide"
                                     :routeTo="'carePost'" />
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import SafetyTechnicsSlide from "@/components/about/safetyTechnics/SafetyTechnicsSlide.vue";
import { defineComponent, onMounted, type Ref, ref } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import type { ICareSlide } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        SafetyTechnicsSlide,
    },
    setup() {
        const careSlides: Ref<ICareSlide[]> = ref([]);
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Благотворительность']}`)
                .then((res) => {
                    careSlides.value = res;
                    console.log(careSlides.value)
                })
        })
        return {
            careSlides,
        };
    },
});
</script>

<template>
    <div class="page__title mt20">Благотворительные проекты</div>

    <VerticalSlider :slides="careSlides"
                    :page="'care'"
                    :modifiers="['needLogo']"
                    :routeTo="'carePost'" />

</template>
<script lang="ts">
import { defineComponent, onMounted, computed, type ComputedRef } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import type { ICareSlide } from "@/interfaces/IEntities";
import { useViewsDataStore } from "@/stores/viewsData";
import VerticalSlider from "@/components/tools/swiper/VerticalSlider.vue";

export default defineComponent({
    components: {
        VerticalSlider
    },
    setup() {
        const careSlides: ComputedRef<ICareSlide[]> = computed(() => useViewsDataStore().getData('careData') as ICareSlide[]);
        onMounted(() => {
            if (careSlides.value.length) return;
            Api.get(`article/find_by/${sectionTips['Благотворительность']}`)
                .then((res) => {
                    console.log(res);

                    useViewsDataStore().setData(res, "careData")
                })

        })
        return {
            careSlides,
        };
    },
});
</script>

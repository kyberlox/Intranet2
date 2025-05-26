<template>
    <div class="experience__page mt20">
        <div class="page__title">Референсы и опыт поставок</div>
        <FlexGallery :page=page
                     :slides="slides"
                     :modifiers="['noFullWidthImg']"
                     :routeTo="'experienceTypes'" />
    </div>
</template>

<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { defineComponent } from "vue";
import { expSlides } from "@/assets/staticJsons/referencesAndExp";
export default defineComponent({
    components: {
        FlexGallery,
    },
    setup() {

        return {
            slides: expSlides,
            page: "experience"
        };
    },
});
</script>

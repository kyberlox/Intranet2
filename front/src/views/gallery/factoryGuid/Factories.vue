<template>
    <div class="experience__page mt20">
        <div class="page__title">Гид по предприятиям </div>
        <FlexGallery :slides="slides"
                     :modifiers="['noFullWidthImg', 'buttons']"
                     :routeTo="'experienceTypes'" />
    </div>
</template>

<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { defineComponent } from "vue";
import { slides } from "@/assets/staticJsons/referencesAndExp";

export default defineComponent({
    components: {
        FlexGallery,
    },
    setup() {
        return {
            slides,
        };
    },
});
</script>

<template>
    <div class="experience__page mt20">
        <div class="page__title">Гид по предприятиям </div>
        <FlexGalleryWithButtons :page=page
                                :slides="slides"
                                :modifiers="['noFullWidthImg']" />
    </div>
</template>

<script lang="ts">
import FlexGalleryWithButtons from "@/components/tools/gallery/FlexGalleryWithButtons.vue";
import { defineComponent } from "vue";
import { slides } from "@/assets/staticJsons/factorySlides";

export default defineComponent({
    components: {
        FlexGalleryWithButtons,
    },
    setup() {
        return {
            slides,
            page: "experience"
        };
    },
});
</script>

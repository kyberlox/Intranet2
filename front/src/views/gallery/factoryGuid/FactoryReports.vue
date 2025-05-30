<template>
    <div class="factory-reports__page mt20">
        <div class="page__title">Репортаж </div>
        <FlexGallery :slides="slides" />
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { factoryReports } from "@/assets/staticJsons/referencesAndExp";

export default defineComponent({
    components: {
        FlexGallery,
    },
    setup() {
        const slides = factoryReports;
        return {
            slides,
        };
    },
});
</script>

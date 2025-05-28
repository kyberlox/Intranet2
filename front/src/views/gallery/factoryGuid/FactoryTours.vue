<template>
    <div class="factory-reports__page mt20">
        <div class="page__title">3D-тур
        </div>
        <FlexGallery :slides="slides"
                     :page="page" />
    </div>
</template>

<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { factoryTours } from "@/assets/staticJsons/factorySlides";
export default {
    components: {
        FlexGallery,
    },
    setup() {
        const slides = factoryTours;
        return {
            slides,
            page: 'tours',
        };
    },
};
</script>

<template>
    <div class="factory-reports__page mt20">
        <div class="page__title">3D-тур
        </div>
        <FlexGallery :slides="slides"
                     :page="page"
                     :routeTo="'factoryTour'" />

    </div>
</template>

<script lang="ts">
import FlexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
export default {
    components: {
        FlexGallery,
    },
    setup() {

        return {
            slides: [],
            page: 'tours',
        };
    },
};
</script>

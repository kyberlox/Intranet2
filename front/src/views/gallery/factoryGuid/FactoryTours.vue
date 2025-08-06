<template>
    <div class="factory-reports__page mt20">
        <div class="page__title">3D-тур </div>
        <ComplexGallery :slides="factoryTours"
                        :routeTo="'factoryTour'" />

    </div>
</template>

<script lang="ts">
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";
import { computed } from "vue";
export default {
    components: {
        ComplexGallery,
    },
    props: {
        id: {
            type: String,
            required: true,
        },
    },
    setup(props) {
        const factoryGuidData = useFactoryGuidDataStore();
        const factoryTours = computed(() => factoryGuidData.getFactoryTours(Number(props.id)));

        return {
            factoryTours
        };
    },
};
</script>

<template>
    <div class="factory-reports__page mt20">
        <div class="page__title">Репортаж </div>
        <ComplexGallery :slides="factoryReports" />
    </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";

export default defineComponent({
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
        const factoryReports = computed(() => factoryGuidData.getFactoryReports(Number(props.id)));

        return {
            factoryReports
        };
    },
});
</script>

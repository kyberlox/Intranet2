<template>
<div v-if="tourFrame"
     class="pano__wrapper mt20">
    <iframe :src="tourFrame"
            width="100%"
            height="100%"
            frameborder="0"></iframe>
</div>
<div v-else
     class="contest__page__loader__wrapper">
    <Loader class="contest__page__loader" />
</div>
</template>

<script lang="ts">
import { ref, computed, watch } from 'vue';
import { defineComponent } from 'vue';
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";
import Loader from "@/components/layout/Loader.vue";

export default defineComponent({
    components: {
        Loader
    },
    props: {
        tourId: {
            type: String
        },
        factory_id: {
            type: String
        }
    },
    setup(props) {
        // loadScript('/src/utils/tour.js')
        const factoryGuid = useFactoryGuidDataStore();
        const currentTour = computed(() => factoryGuid.getFactoryTour(Number(props.factory_id), String(props.tourId)))

        const tourFrame = ref();

        watch((currentTour), () => {
            if (currentTour.value) {
                tourFrame.value = `https://intranet.emk.ru/api/files/tours/${currentTour.value?.["3D_files_path"]}/index.html`;
            }
        }, { immediate: true, deep: true })

        return {
            tourFrame
        }
    }
});
</script>

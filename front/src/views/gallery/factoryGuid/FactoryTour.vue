<template>
    <div class="pano__wrapper mt20"
         id="wrapper">
        <div class="pano"
             id="pano"></div>
    </div>
</template>

<script lang="ts">
import { loadScript, unloadScript } from "vue-plugin-load-script";
import { ref, onBeforeMount, onUnmounted, computed } from 'vue';
import { defineComponent } from 'vue';
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";

export default defineComponent({
    props: {
        id: {
            type: String
        },
        factoryId: {
            type: String
        }
    },
    setup(props) {
        const factoryGuid = useFactoryGuidDataStore();
        const currentTour = computed(() => factoryGuid.getFactoryTour(Number(props.factoryId), String(props.id)))

        const folder = ref('');
        const swf = ref();
        const xml = ref();
        const basePath = '/src/assets/factoryTour/';

        onBeforeMount(() => {
            folder.value = "3d-01";
            swf.value = `${basePath}${folder.value}/tour.swf`;
            xml.value = `${basePath}${folder.value}/tour.xml`;
            loadScript('/src/utils/tour.js').then(() => {
                if (folder.value) {
                    window.embedpano({
                        swf: swf.value,
                        xml: xml.value,
                        target: "pano",
                        html5: "auto",
                        mobilescale: 1.0,
                        passQueryParameters: true
                    });
                }
            })
        })

        onUnmounted(() => {
            if (window.removepano) {
                window.removepano("pano");
            }
            unloadScript('/src/utils/tour.js');
        })
    }
});
</script>
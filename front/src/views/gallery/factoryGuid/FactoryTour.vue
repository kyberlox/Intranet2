<template>
<div class="pano__wrapper mt20"
     id="wrapper">
    <div class="pano"
         id="pano"></div>
</div>
</template>

<script lang="ts">
import { loadScript, unloadScript } from "vue-plugin-load-script";
import { ref, onBeforeMount, onUnmounted, computed, watchEffect } from 'vue';
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

        watchEffect(() => {
            if (currentTour.value) {
                const basePath = `https://intranet.emk.ru/tours/${currentTour.value?.["3D_files_path"]}`;
                swf.value = `${basePath}/tour.swf`;
                xml.value = `${basePath}/pano.xml`;
                loadScript('/src/utils/tour.js').then(() => {
                    window.embedpano({
                        swf: swf.value,
                        xml: xml.value,
                        target: "pano",
                        html5: "auto",
                        mobilescale: 1.0,
                        passQueryParameters: true,
                    });
                })
            }
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
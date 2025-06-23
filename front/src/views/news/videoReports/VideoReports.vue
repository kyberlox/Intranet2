<template>
    <h1 class="page__title mt20">Видеорепортажи</h1>
    <GridGallery class="mt20"
                 :gallery="videoReports"
                 :routeTo="'videoReport'"
                 :type="'video'" />
</template>
<script lang="ts">
import GridGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import { defineComponent, onMounted, computed, type ComputedRef } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from "@/stores/loadingStore";
import type { IVideoReports } from "@/interfaces/IEntities";
export default defineComponent({
    components: { GridGallery },
    setup() {
        const viewsData = useViewsDataStore();
        const videoReports: ComputedRef<IVideoReports[]> = computed(() => viewsData.getData('videoReportsData') as IVideoReports[]);
        onMounted(() => {
            if (videoReports.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Видеорепортажи']}`)
                .then(res => {
                    viewsData.setData(res, 'videoReportsData');
                })
                .finally(() => useLoadingStore().setLoadingStatus(false));
        });

        return {
            videoReports,
        };
    },
});
</script>

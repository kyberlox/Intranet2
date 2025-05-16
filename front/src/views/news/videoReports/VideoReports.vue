<template>
    <div class="page__wrapper mt20">
        <h1 class="page__title">Видеорепортажи</h1>
        <GridGallery class="mt20"
                     :gallery="videoReports"
                     :routeTo="'videoreport'"
                     :type="'video'" />
    </div>
</template>
<script lang="ts">
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import { defineComponent, onMounted, computed } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from "@/stores/loadingStore";
export default defineComponent({
    components: { GridGallery },
    setup() {
        const viewsData = useViewsDataStore();
        const videoReports = computed(() => viewsData.getData('videoReportsData'));
        onMounted(() => {
            if (videoReports.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Видеорепортажи']}`)
                .then(res => {
                    viewsData.setData(res, 'videoReportsData');
                })
                .finally(() => useLoadingStore().setLoadingStatus(false));

        })
        return {
            videoReports,
        };
    },
});
</script>

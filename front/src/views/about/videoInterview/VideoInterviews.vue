<template>
    <div class="page__wrapper mt20">
        <h1 class="page__title">Видеоинтервью</h1>
        <GridGallery class="mt20"
                     :gallery="interviews"
                     :routeTo="'videoInterview'"
                     :type="'video'" />
    </div>
</template>
<script lang="ts">
import { defineComponent, onMounted, computed } from "vue";
import GridGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData"
import { useLoadingStore } from "@/stores/loadingStore";
import type { IVideoInterview } from "@/interfaces/IEntities";

export default defineComponent({
    components: { GridGallery },
    setup() {
        const viewsData = useViewsDataStore();
        const interviews = computed((): IVideoInterview[] => viewsData.getData('videoInterviewsData') as IVideoInterview[]);

        onMounted(() => {
            if (interviews.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Видеоинтервью']}`)
                .then(res => {
                    viewsData.setData(res, 'videoInterviewsData')
                })
                .finally(() => {
                    useLoadingStore().setLoadingStatus(false);
                })
        })
        return {
            interviews,
        };
    },
});
</script>

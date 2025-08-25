<template>
    <h1 class="page__title mt20">Видеорепортажи</h1>
    <div class="page__filter">
        <DateFilter :params="filterYears"
                    :buttonText="currentYear ?? 'Год'"
                    @pickFilter="(year: string) => currentYear = year" />
        <TagsFilter @pickTag="(tag: string) => currentTag = tag" />
    </div>
    <GridGallery class="mt20"
                 :gallery="videoReports"
                 :routeTo="'videoReport'"
                 :type="'video'" />
</template>
<script lang="ts">
import GridGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import { defineComponent, onMounted, computed, type ComputedRef, ref, type Ref } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from "@/stores/loadingStore";
import type { INews } from "@/interfaces/IEntities";
import DateFilter from '@/components/tools/common/DateFilter.vue';
import TagsFilter from '@/components/tools/common/TagsFilter.vue';

export default defineComponent({
    components: {
        GridGallery,
        DateFilter,
        TagsFilter
    },
    setup() {
        const viewsData = useViewsDataStore();
        const videoReports: ComputedRef<INews[]> = computed(() => viewsData.getData('videoReportsData') as INews[]);
        const currentTag: Ref<string> = ref('');
        const currentYear: Ref<string> = ref('');
        const filterYears: Ref<string[]> = ref([]);

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
            currentTag,
            currentYear,
            filterYears
        };
    },
});
</script>

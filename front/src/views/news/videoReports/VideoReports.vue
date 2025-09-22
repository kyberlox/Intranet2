<template>
<h1 class="page__title mt20">Видеорепортажи</h1>
<div class="page__filter">
    <DateFilter :params="filterYears"
                :buttonText="currentYear ?? 'Год'"
                @pickFilter="(year: string) => currentYear = year" />
    <TagsFilter @pickTag="(tag: string) => currentTag = tag" />
</div>
<div class="row">
    <GridGallery v-if="!emptyTag"
                 class="mt20"
                 :gallery="visibleReports"
                 :routeTo="'videoReport'"
                 :type="'video'" />
    <p class="mt20"
       v-else>Нет новостей в этой категории</p>
</div>
</template>
<script lang="ts">
import GridGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import { defineComponent, onMounted, computed, type ComputedRef, ref, type Ref, watch } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from "@/stores/loadingStore";
import type { INews } from "@/interfaces/IEntities";
import DateFilter from '@/components/tools/common/DateFilter.vue';
import TagsFilter from '@/components/tools/common/TagsFilter.vue';
import { useNewsFilterWatch } from "@/composables/useNewsFilterWatch";
import { extractYears } from "@/utils/extractYearsFromPosts";

export default defineComponent({
    components: {
        GridGallery,
        DateFilter,
        TagsFilter
    },
    setup() {
        const viewsData = useViewsDataStore();
        const videoReports: ComputedRef<INews[]> = computed(() => viewsData.getData('videoReportsData') as INews[]);
        const visibleReports: Ref<INews[]> = ref(videoReports.value);
        const currentTag: Ref<string> = ref('');
        const currentYear: Ref<string> = ref('');
        const filterYears: Ref<string[]> = ref([]);
        const emptyTag: Ref<boolean> = ref(false);

        watch(([currentTag, currentYear]), async () => {
            const { newVisibleNews, newEmptyTag, newFilterYears } =
                await useNewsFilterWatch(currentTag, currentYear, videoReports);

            visibleReports.value = newVisibleNews.value;
            emptyTag.value = newEmptyTag.value;
            filterYears.value = newFilterYears.value;
        })

        onMounted(() => {
            if (videoReports.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Видеорепортажи']}`)
                .then(res => {
                    viewsData.setData(res, 'videoReportsData');
                    visibleReports.value = res;
                })
                .finally(() => {
                    filterYears.value = extractYears(visibleReports.value);
                    useLoadingStore().setLoadingStatus(false)
                });
        });

        return {
            videoReports,
            currentTag,
            currentYear,
            filterYears,
            visibleReports,
            emptyTag
        };
    },
});
</script>

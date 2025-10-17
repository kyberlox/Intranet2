<template>
<h1 class="page__title mt20">Видеорепортажи</h1>
<div class="tags__page__filter">
    <div>
        <button @click="showFilter = !showFilter"
                class="btn btn-light dropdown-toggle tagDateNavBar__dropdown-toggle">
            Год публикации
        </button>
        <DateFilter v-if="showFilter"
                    :params="filterYears"
                    :buttonText="currentYear ?? 'Год'"
                    @pickFilter="(year: string) => currentYear = year" />
    </div>
    <TagsFilter @pickTag="(tag: string) => currentTag = tag"
                :tagId="tagId" />
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
    props: {
        tagId: String
    },
    setup(props) {
        const viewsData = useViewsDataStore();
        const videoReports: ComputedRef<INews[]> = computed(() => viewsData.getData('videoReportsData') as INews[]);
        const visibleReports: Ref<INews[]> = ref([]);
        const currentTag: Ref<string> = ref('');
        const currentYear: Ref<string> = ref('');
        const filterYears: Ref<string[]> = ref([]);
        const emptyTag: Ref<boolean> = ref(false);
        const showFilter = ref(false);

        watch(([currentTag, currentYear]), async () => {
            const { newVisibleNews, newEmptyTag, newFilterYears } =
                await useNewsFilterWatch(currentTag, currentYear, videoReports, sectionTips['Видеорепортажи']);

            visibleReports.value = newVisibleNews.value;
            emptyTag.value = newEmptyTag.value;
            filterYears.value = newFilterYears.value;
            showFilter.value = false;
        })

        onMounted(() => {
            if (videoReports.value.length) return;
            Api.get(`article/find_by/${sectionTips['Видеорепортажи']}`)
                .then(res => {
                    viewsData.setData(res, 'videoReportsData');
                    if (!props.tagId) {
                        visibleReports.value = res;
                    }
                })
                .finally(() => {
                    filterYears.value = extractYears(visibleReports.value);
                });
        });

        return {
            videoReports,
            currentTag,
            currentYear,
            filterYears,
            visibleReports,
            emptyTag,
            showFilter
        };
    },
});
</script>

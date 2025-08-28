<template>
    <div class="page__title mt20">Актуальные новости</div>
    <div class="page__filter">
        <DateFilter :params="filterYears"
                    :buttonText="currentYear ?? 'Год'"
                    @pickFilter="(year: string) => currentYear = year" />
        <TagsFilter @pickTag="(tag: string) => currentTag = tag" />
    </div>
    <div class="row">
        <SampleGallery v-if="!emptyTag"
                       :gallery="visibleNews"
                       :type="'postPreview'"
                       :routeTo="'actualArticle'"
                       :modifiers="['noReactionUpdates']" />
        <p class="mt20"
           v-else>Нет новостей в этой категории</p>
    </div>
</template>
<script lang="ts">
import { sectionTips } from '@/assets/static/sectionTips';
import SampleGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import Api from '@/utils/Api';
import { defineComponent, onMounted, type Ref, ref, computed, type ComputedRef, watch } from 'vue';
import type { INews } from '@/interfaces/IEntities';
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from '@/utils/showEventsByYear';
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from '@/stores/loadingStore';
import DateFilter from '@/components/tools/common/DateFilter.vue';
import TagsFilter from '@/components/tools/common/TagsFilter.vue';
import { useNewsFilterWatch } from '@/composables/useNewsFilterWatch';

export default defineComponent({
    components: {
        SampleGallery,
        DateFilter,
        TagsFilter
    },
    setup() {
        const viewsData = useViewsDataStore();
        const allNews: ComputedRef<INews[]> = computed(() => viewsData.getData('actualNewsData') as INews[]);
        const visibleNews: Ref<INews[]> = ref(allNews.value);
        const currentTag: Ref<string> = ref('');
        const currentYear: Ref<string> = ref('');
        const filterYears: Ref<string[]> = ref([]);
        const emptyTag: Ref<boolean> = ref(false);

        watch(([currentTag, currentYear]), async () => {
            const { newVisibleNews, newEmptyTag, newFilterYears } =
                await useNewsFilterWatch(currentTag, currentYear, allNews, visibleNews);

            visibleNews.value = newVisibleNews.value;
            emptyTag.value = newEmptyTag.value;
            filterYears.value = newFilterYears.value;
        })

        onMounted(async () => {
            if (allNews.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            await Api.get(`article/find_by/${sectionTips['АктуальныеНовости']}`)
                .then((res) => {
                    viewsData.setData(res, 'actualNewsData');
                    visibleNews.value = res;
                })
                .finally(() => {
                    filterYears.value = extractYears(visibleNews.value);
                    useLoadingStore().setLoadingStatus(false);
                })
        })

        return {
            allNews,
            visibleNews,
            extractYears,
            showEventsByYear,
            currentYear,
            currentTag,
            filterYears,
            emptyTag
        };
    },
});
</script>
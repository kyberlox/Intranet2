<template>
    <div class="page__title mt20">Актуальные новости</div>
    <div class="page__filter">
        <DateFilter :params="filterYears"
                    :buttonText="currentYear ?? 'Год'"
                    @pickFilter="(year) => currentYear = year" />
        <TagsFilter @pickTag="(tag) => currentTag = tag" />
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
        const currentTag = ref('');
        const currentYear = ref('');
        const filterYears = ref([]);
        const emptyTag = ref();

        watch(([currentTag, currentYear]), () => {
            if (currentTag.value && currentYear.value || currentTag.value && !currentYear.value) {
                const newData = ref();
                Api.get(`article/get_articles_by_tag_id/${sectionTips['Актуальные новости']}/${currentTag.value}`)
                    .then((data) => newData.value = data.filter((e) => {
                        return e.date_creation?.includes(currentYear.value)
                    }))
                    .finally(() => {
                        if (!newData.value.length) return emptyTag.value = true;
                        visibleNews.value = newData.value;
                        filterYears.value = extractYears(visibleNews.value);
                        emptyTag.value = false;
                    })
            }
            else if ((!currentTag.value && currentYear.value) || (!currentTag.value && !currentYear.value)) {
                filterYears.value = extractYears(visibleNews.value);
                visibleNews.value = allNews.value.filter((e) => {
                    return e.date_creation?.includes(currentYear.value)
                })
                return visibleNews.value.length ? emptyTag.value = false : emptyTag.value = true;
            }
        })

        onMounted(() => {
            if (allNews.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Актуальные новости']}`)
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
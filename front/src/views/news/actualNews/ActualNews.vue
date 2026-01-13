<template>
<h1 class="page__title mt20">Актуальные новости</h1>
<div class="tags__page__filter">
    <div>
        <button @click="showFilter = !showFilter"
                class="btn dropdown-toggle tagDateNavBar__dropdown-toggle">
            {{ currentYear || 'Год публикации' }}
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
    <SampleGallery v-if="!emptyTag"
                   :gallery="visibleNews"
                   :type="'postPreview'"
                   :routeTo="'actualArticle'" />
    <p v-else
       class="mt20">Нет новостей в этой категории</p>
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
import DateFilter from '@/components/tools/common/DateFilter.vue';
import TagsFilter from '@/components/tools/common/TagsFilter.vue';
import { useNewsFilterWatch } from '@/composables/useNewsFilterWatch';

export default defineComponent({
    components: {
        SampleGallery,
        DateFilter,
        TagsFilter
    },
    props: {
        id: {
            type: Number
        },
        tagId: {
            type: String
        }
    },
    setup(props) {
        const viewsData = useViewsDataStore();
        const allNews: ComputedRef<INews[]> = computed(() => viewsData.getData('actualNewsData') as INews[]);
        const visibleNews: Ref<INews[]> = ref([]);
        const currentTag: Ref<string> = ref('');
        const currentYear: Ref<string> = ref('');
        const filterYears: Ref<string[]> = ref([]);
        const emptyTag: Ref<boolean> = ref(false);
        const showFilter = ref(false);

        watch(([currentTag, currentYear]), async () => {
            const { newVisibleNews, newEmptyTag, newFilterYears } =
                await useNewsFilterWatch(currentTag, currentYear, allNews, sectionTips['АктуальныеНовости']);

            visibleNews.value = newVisibleNews.value;
            emptyTag.value = newEmptyTag.value;
            filterYears.value = newFilterYears.value;
            showFilter.value = false;
        })

        onMounted(() => {
            if (allNews.value.length && !props.tagId) {
                visibleNews.value = allNews.value;
                filterYears.value = extractYears(allNews.value);
            } else
                Api.get(`article/find_by/${sectionTips['АктуальныеНовости']}`)
                    .then((res) => {
                        viewsData.setData(res, 'actualNewsData');
                        if (!props.tagId) visibleNews.value = res;
                    })
                    .finally(() => {
                        filterYears.value = extractYears(visibleNews.value);
                    })
        })

        return {
            allNews,
            visibleNews,
            currentYear,
            currentTag,
            filterYears,
            emptyTag,
            showFilter,
            extractYears,
            showEventsByYear,
        };
    },
});
</script>

<template>
<h1 class="page__title mt20">
    {{ pageTitle }}
</h1>
<div class="tags__page__filter">
    <div v-if="needYears">
        <button @click="showFilter = !showFilter"
                class="btn dropdown-toggle tagDateNavBar__dropdown-toggle">
            {{ currentYear || 'Год публикации' }}
        </button>
        <DateFilter v-if="showFilter"
                    :params="filterYears"
                    :buttonText="currentYear ?? 'Год'"
                    @pickFilter="(year: string) => currentYear = year" />
    </div>
    <TagsFilter v-if="needTags"
                @pickTag="(tag: string) => currentTag = tag"
                :tagId="tagId" />
</div>
<div class="row">
    <ContentPlug v-if="!isLoading && (!visibleNews || !visibleNews.length)"
                 :needGptMark="true"
                 :plugImg="emptyPlug"
                 :plugText="emptyPageHtml" />

    <ComplexGallery v-else-if="!emptyTag && galleryType == 'complex'"
                    class="mt20"
                    :page="'postPreview'"
                    :slides="(visibleNews as IBaseEntity[])"
                    :routeTo="routeTo" />

    <SampleGallery v-else-if="!emptyTag && galleryType == 'sample'"
                   :gallery="visibleNews"
                   :type="'postPreview'"
                   :routeTo="routeTo" />
    <p v-else
       class="mt20">Нет новостей в этой категории</p>
</div>
<PageSelector v-if="paginationEnabled"
              :isLoading="isLoading"
              @loadMore="fetchNews" />
</template>
<script lang="ts">
import SampleGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import Api from '@/utils/Api';
import { defineComponent, onMounted, onUnmounted, type Ref, ref, computed, type ComputedRef, watch, type PropType } from 'vue';
import type { IBaseEntity, INews } from '@/interfaces/IEntities';
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from '@/utils/showEventsByYear';
import { useViewsDataStore } from "@/stores/viewsData";
import DateFilter from '@/components/tools/common/DateFilter.vue';
import TagsFilter from '@/components/tools/common/TagsFilter.vue';
import { useNewsFilterWatch } from '@/composables/useNewsFilterWatch';
import { type DataStateKey } from "@/stores/viewsData";
import { emptyPageHtml } from '@/assets/static/contentPlugs';
import emptyPlug from '@/assets/imgs/plugs/contentPlugEmpty.jpg';
import ContentPlug from "./ContentPlug.vue";
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { featureFlags } from "@/assets/static/featureFlags";
import PageSelector from "@/components/tools/common/PageSelector.vue";
export default defineComponent({
    components: {
        SampleGallery,
        DateFilter,
        TagsFilter,
        ContentPlug,
        ComplexGallery,
        PageSelector
    },
    props: {
        id: {
            type: Number
        },
        pageTitle: {
            type: String
        },
        needTags: {
            type: Boolean,
            default: false
        },
        needYears: {
            type: Boolean,
            default: true
        },
        tagId: {
            type: String
        },
        sectionId: {
            type: Number,
            required: true
        },
        storeItemsName: {
            type: String as PropType<DataStateKey>,
            required: true
        },
        type: {
            type: String
        },
        routeTo: {
            type: String
        },
        galleryType: {
            type: String,
            default: () => 'sample'
        },
        needPagination: {
            type: Boolean,
            default: false
        }
    },
    setup(props) {
        const abortController = new AbortController();
        const viewsData = useViewsDataStore();
        const allNews: ComputedRef<INews[]> = computed(() => viewsData.getData(props.storeItemsName) as INews[]);
        const visibleNews: Ref<INews[]> = ref([]);
        const currentTag: Ref<string> = ref('');
        const currentYear: Ref<string> = ref('');
        const filterYears: Ref<string[]> = ref([]);
        const emptyTag: Ref<boolean> = ref(false);
        const showFilter = ref(false);
        const isLoading = ref(true);
        const offset = ref(0);
        const paginationEnabled = computed(() => featureFlags.pagination && props.needPagination);
        const isLimit = ref(true);

        const fetchNews = async (tag?: number, year?: number) => {
            isLoading.value = true;
            const paginationQuery = paginationEnabled.value ? `?offset=${offset.value}&limit=15${year ? `&year=${year}` : ''}${tag ? `&tag=${tag}` : ''}` : '';

            try {
                const res = await Api.get(`article/find_by/${props.sectionId}${paginationQuery}`, null, abortController.signal)
                if (offset.value == 0) { viewsData.setData(res, props.storeItemsName) }
                offset.value += 15;
                visibleNews.value = visibleNews.value.concat(res);
            } catch (error) {
                console.error(error)
            }
            finally {
                isLoading.value = false;
            }
        }

        watch(([currentTag, currentYear]), async () => {
            offset.value = 0;
            visibleNews.value.length = 0;
            allNews.value.length = 0;
            viewsData.setData(allNews.value, props.storeItemsName);
            // const { newVisibleNews, newEmptyTag, newFilterYears } =
            //     await useNewsFilterWatch(currentTag, currentYear, allNews, String(props.sectionId));

            // visibleNews.value = newVisibleNews.value;
            // emptyTag.value = newEmptyTag.value;
            // filterYears.value = newFilterYears.value;
            showFilter.value = false;

            fetchNews(Number(currentTag.value), Number(currentYear.value))
        })

        const yearsInit = () => {
            const yearStart = new Date().getFullYear();
            const yearEnd = 2018;
            for (let index = yearStart; index > yearEnd; index -= 1) {
                filterYears.value.push(String(index))
            }
        }

        onMounted(async () => {
            yearsInit();
            if (allNews.value && allNews.value.length && !props.tagId) {
                visibleNews.value = allNews.value;
            } else
                await fetchNews();
        })

        onUnmounted(() => {
            abortController?.abort();
        })


        return {
            allNews,
            visibleNews,
            currentYear,
            currentTag,
            filterYears,
            emptyTag,
            emptyPageHtml,
            emptyPlug,
            showFilter,
            isLoading,
            paginationEnabled,
            isLimit,
            extractYears,
            showEventsByYear,
            fetchNews,
        };
    },
});
</script>

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
<PageSelector v-if="paginationEnabled && visibleNews && visibleNews.length"
              :isLimit="isLimit"
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
            default: true
        }
    },
    setup(props) {
        let abortController: null | AbortController = null;
        const viewsData = useViewsDataStore();
        const allNews: ComputedRef<INews[]> = computed(() => viewsData.getData(props.storeItemsName) as INews[]);
        const visibleNews: Ref<INews[]> = ref([]);
        const currentTag: Ref<string> = ref('');
        const currentYear: Ref<string> = ref('');
        const filterYears: Ref<string[]> = ref([]);
        const emptyTag: Ref<boolean> = ref(false);
        const showFilter = ref(false);
        const isLoading = ref(false);
        const offset = ref(0);
        const paginationEnabled = computed(() => featureFlags.pagination && props.needPagination);
        const isLimit = ref(false);

        const fetchNews = async () => {
            if (abortController) {
                abortController?.abort();
            }
            abortController = new AbortController();
            isLimit.value = false;
            isLoading.value = true;
            const paginationQuery = paginationEnabled.value ? `?offset=${offset.value}&limit=15${currentYear.value ? `&year=${currentYear.value}` : ''}${currentTag.value ? `&tag=${currentTag.value}` : ''}` : '';
            try {
                const res = await Api.get(`article/find_by/${props.sectionId}${paginationQuery}`, null, abortController.signal)
                if (offset.value == 0) { viewsData.setData(res, props.storeItemsName) }
                if (res.length == 0 || res.length < 15) {
                    isLimit.value = true;
                }
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
            showFilter.value = false;
            refreshNews();
            fetchNews();
        })

        const yearsInit = () => {
            const yearStart = new Date().getFullYear();
            const yearEnd = 2018;
            for (let index = yearStart; index >= yearEnd; index -= 1) {
                filterYears.value.push(String(index))
            }
        }

        const refreshNews = () => {
            if (currentTag.value || currentYear.value) {
                offset.value = 0;
                visibleNews.value.length = 0;
                if (allNews.value) {
                    allNews.value.length = 0;
                }
                viewsData.setData(allNews.value, props.storeItemsName);
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

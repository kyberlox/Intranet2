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
    <ContentPlug v-if="!isLoading && !visibleNews.length"
                 :needGptMark="true"
                 :plugImg="emptyPlug"
                 :plugText="emptyPageHtml" />

    <ComplexGallery v-else-if="!emptyTag"
                    class="mt20"
                    :page="'postPreview'"
                    :slides="visibleNews"
                    :routeTo="routeTo" />
</div>
</template>

<script lang="ts">
import Api from '@/utils/Api';
import { emptyPageHtml } from '@/assets/static/contentPlugs';
import emptyPlug from '@/assets/imgs/plugs/contentPlugEmpty.jpg';
import { defineComponent, onMounted, type Ref, ref, computed, type ComputedRef, watch, type PropType } from 'vue';
import type { IBaseEntity } from '@/interfaces/IEntities';
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from '@/utils/showEventsByYear';
import { useViewsDataStore } from "@/stores/viewsData";
import DateFilter from '@/components/tools/common/DateFilter.vue';
import TagsFilter from '@/components/tools/common/TagsFilter.vue';
import { useNewsFilterWatch } from '@/composables/useNewsFilterWatch';
import { type DataStateKey } from "@/stores/viewsData";
import ComplexGallery from '@/components/tools/gallery/complex/ComplexGallery.vue';
import ContentPlug from '../ContentPlug.vue';

export default defineComponent({
    components: {
        ComplexGallery,
        DateFilter,
        TagsFilter,
        ContentPlug
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
        }
    },
    setup(props) {
        const isLoading = ref(true);
        const viewsData = useViewsDataStore();
        const allNews: ComputedRef<IBaseEntity[]> = computed(() => viewsData.getData(props.storeItemsName) as IBaseEntity[]);
        const visibleNews: Ref<IBaseEntity[]> = ref([]);
        const currentTag: Ref<string> = ref('');
        const currentYear: Ref<string> = ref('');
        const filterYears: Ref<string[]> = ref([]);
        const emptyTag: Ref<boolean> = ref(false);
        const showFilter = ref(false);

        watch(([currentTag, currentYear]), async () => {
            const { newVisibleNews, newEmptyTag, newFilterYears } =
                await useNewsFilterWatch(currentTag, currentYear, allNews, String(props.sectionId));

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
                isLoading.value = true;
            Api.get(`article/find_by/${props.sectionId}`)
                .then((res) => {
                    viewsData.setData(res, props.storeItemsName);
                    if (!props.tagId) visibleNews.value = res;
                })
                .finally(() => {
                    filterYears.value = extractYears(visibleNews.value);
                    isLoading.value = false;
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
            emptyPageHtml,
            emptyPlug,
            isLoading,
            extractYears,
            showEventsByYear,
        };
    },
});
</script>

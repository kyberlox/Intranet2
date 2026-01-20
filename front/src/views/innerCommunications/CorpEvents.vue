<template>
<h1 class="page__title mt20">Корпоративные события</h1>
<div class="tags__page__filter">
    <div>
        <button @click="showFilter = !showFilter"
                class="btn dropdown-toggle tagDateNavBar__dropdown-toggle">
            {{ currentYear || 'Год публикации' }}
        </button>
        <DateFilter v-if="allEvents && showFilter"
                    :buttonText="buttonText"
                    :params="filterYears"
                    @pickFilter="(year: string) => currentYear = year" />
    </div>
    <TagsFilter @pickTag="(tag: string) => currentTag = tag" />
</div>
<div class="row">
    <SampleGallery v-if="visibleEvents && !emptyTag"
                   :gallery="visibleEvents"
                   :routeTo="'corpEvent'" />
    <p v-else
       class="mt20">Нет новостей в этой категории</p>
</div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref, type Ref, type ComputedRef, watch } from "vue";
import DateFilter from "@/components/tools/common/DateFilter.vue";
import SampleGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { extractYears } from "@/utils/extractYearsFromPosts";
import type { INews } from "@/interfaces/IEntities";
import { showEventsByYear } from "@/utils/showEventsByYear";
import { useViewsDataStore } from "@/stores/viewsData";
import { useNewsFilterWatch } from "@/composables/useNewsFilterWatch";
import TagsFilter from "@/components/tools/common/TagsFilter.vue";

export default defineComponent({
    components: { SampleGallery, DateFilter, TagsFilter },
    props: {
        pageTitle: String,
        id: Number,
        tagId: String
    },
    setup(props) {
        const allEvents: ComputedRef<INews[]> = computed(() => useViewsDataStore().getData('corpEventsData') as INews[]);
        const visibleEvents = ref<INews[]>();
        const buttonText: Ref<string> = ref('Год публикации');
        const showFilter = ref(false);
        const currentTag: Ref<string> = ref(props.tagId ? props.tagId : '');
        const emptyTag: Ref<boolean> = ref(false);
        const filterYears: Ref<string[]> = ref([]);
        const currentYear: Ref<string> = ref('');

        watch(([currentTag, currentYear]), async () => {
            if (currentTag.value || currentYear.value) {
                const { newVisibleNews, newEmptyTag, newFilterYears } =
                    await useNewsFilterWatch(currentTag, currentYear, allEvents, sectionTips['КорпоративныеСобытия']);
                console.log(newVisibleNews.value);

                visibleEvents.value = newVisibleNews.value;
                emptyTag.value = newEmptyTag.value;
                filterYears.value = newFilterYears.value;
                showFilter.value = false;
            }
        }, { immediate: true, deep: true })

        onMounted(() => {
            if (!allEvents.value.length && !currentTag.value) {
                Api.get(`article/find_by/${sectionTips['КорпоративныеСобытия']}`)
                    .then(res => {
                        useViewsDataStore().setData(res, 'corpEventsData');
                        visibleEvents.value = res;
                        filterYears.value = extractYears(allEvents.value);
                    })
            }
        })

        const filterYear = (year: string) => {
            if (!year) {
                visibleEvents.value = allEvents.value;
                buttonText.value = 'Год публикации';
            }
            else {
                buttonText.value = year;
                visibleEvents.value = showEventsByYear(allEvents.value, year);
            }
            showFilter.value = false;
            console.log(visibleEvents.value);

        }

        return {
            visibleEvents,
            allEvents,
            buttonText,
            showFilter,
            currentTag,
            emptyTag,
            filterYears,
            currentYear,
            extractYears,
            showEventsByYear,
            filterYear
        };
    },
});
</script>

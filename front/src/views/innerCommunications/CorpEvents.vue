<template>
    <h1 class="page__title mt20">Корпоративные события</h1>
    <DateFilter v-if="allEvents"
                :buttonText="buttonText"
                :params="extractYears(allEvents)"
                @pickFilter="(year: string) => filterYear(year)" />
    <SampleGallery v-if="visibleEvents"
                   :gallery="visibleEvents"
                   :routeTo="'corpEvent'" />
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
import { useLoadingStore } from "@/stores/loadingStore";

export default defineComponent({
    components: { SampleGallery, DateFilter },
    props: {
        pageTitle: String,
        id: Number,
    },
    setup() {
        const allEvents: ComputedRef<INews[]> = computed(() => useViewsDataStore().getData('corpEventsData') as INews[]);
        const visibleEvents = ref<INews[]>(allEvents.value);
        const buttonText: Ref<string> = ref('Год публикации');

        onMounted(() => {
            if (allEvents.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['КорпоративныеСобытия']}`)
                .then(res => {
                    useViewsDataStore().setData(res, 'corpEventsData')
                    visibleEvents.value = res;
                })
                .finally(() => {
                    useLoadingStore().setLoadingStatus(false);
                })
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
        }

        return {
            visibleEvents,
            allEvents,
            buttonText,
            extractYears,
            showEventsByYear,
            filterYear
        };
    },
});
</script>

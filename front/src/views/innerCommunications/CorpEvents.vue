<template>
    <h2 class="page__title mt20">Корпоративные события</h2>
    <TagDateNavBar v-if="allEvents"
                   :years="extractYears(allEvents)"
                   :modifiers="'noTag'"
                   @pickYear="(year) => visibleEvents = showEventsByYear(allEvents, year)" />
    <GridGallery v-if="visibleEvents"
                 :gallery="visibleEvents"
                 :routeTo="'corpEvent'" />
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref, type ComputedRef } from "vue";
import TagDateNavBar from "@/components/TagDateNavBar.vue";
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import { extractYears } from "@/utils/extractYearsFromPosts";
import type { ICorpEventsItem } from "@/interfaces/IEntities";
import { showEventsByYear } from "@/utils/showEventsByYear";
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from "@/stores/loadingStore";

export default defineComponent({
    components: { GridGallery, TagDateNavBar },
    props: {
        pageTitle: String,
        id: Number,
    },

    setup() {
        const allEvents: ComputedRef<ICorpEventsItem[]> = computed(() => useViewsDataStore().getData('corpEventsData') as ICorpEventsItem[]);
        const visibleEvents = ref<ICorpEventsItem[]>(allEvents.value);
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

        return {
            visibleEvents,
            extractYears,
            allEvents,
            showEventsByYear
        };
    },
});
</script>

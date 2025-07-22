<template>
    <h1 class="page__title mt20">Корпоративные события</h1>
    <TagDateNavBar v-if="allEvents"
                   :years="extractYears(allEvents)"
                   :modifiers="'noTag'"
                   @pickYear="(year: string) => visibleEvents = showEventsByYear(allEvents, year)" />
    <GridGallery v-if="visibleEvents"
                 :gallery="visibleEvents"
                 :routeTo="'corpEvent'" />
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref, type ComputedRef } from "vue";
import TagDateNavBar from "@/components/tools/common/TagDateNavBar.vue";
import GridGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { extractYears } from "@/utils/extractYearsFromPosts";
import type { INews } from "@/interfaces/IEntities";
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
        const allEvents: ComputedRef<INews[]> = computed(() => useViewsDataStore().getData('corpEventsData') as INews[]);
        const visibleEvents = ref<INews[]>(allEvents.value);
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

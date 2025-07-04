<template>
    <div class="page__title mt20">Официальные события</div>
    <TagDateNavBar :years="extractYears(allSlides)"
                   :modifiers="'noTag'"
                   @pickYear="(year: string) => visibleEvents = showEventsByYear(allSlides, year)" />
    <FlexGallery v-if="visibleEvents"
                 class="mt20"
                 :page=page
                 :slides="visibleEvents"
                 :routeTo="'officialEvent'" />
</template>
<script lang="ts">
import TagDateNavBar from '@/components/tools/common/TagDateNavBar.vue';
import FlexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { computed, defineComponent, onMounted, ref, type Ref } from 'vue';
import Api from '@/utils/Api';
import { sectionTips } from '@/assets/static/sectionTips';
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from "@/utils/showEventsByYear";
import { useViewsDataStore } from '@/stores/viewsData';
import { useLoadingStore } from '@/stores/loadingStore';
import type { IOfficialEvents } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        TagDateNavBar,
        FlexGallery
    },
    setup() {
        const allSlides = computed((): IOfficialEvents[] => useViewsDataStore().getData('officialEventsData') as IOfficialEvents[]);
        const visibleEvents: Ref<IOfficialEvents[]> = ref(allSlides.value);
        onMounted(() => {
            if (allSlides.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['офСобытия']}`)
                .then((res) => {
                    useViewsDataStore().setData(res, 'officialEventsData');
                    visibleEvents.value = res;
                })
                .finally(() => {
                    useLoadingStore().setLoadingStatus(false);
                })
        })
        return {
            allSlides,
            page: 'officialEvents',
            extractYears,
            visibleEvents,
            showEventsByYear
        };
    },
});
</script>
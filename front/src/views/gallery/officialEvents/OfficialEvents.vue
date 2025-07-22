<template>
    <div class="page__title mt20">Официальные события</div>
    <TagDateNavBar :years="extractYears(allSlides)"
                   :modifiers="'noTag'"
                   @pickYear="(year: string) => visibleEvents = showEventsByYear(allSlides, year)" />
    <ComplexGallery v-if="visibleEvents"
                    class="mt20"
                    :page=page
                    :slides="visibleEvents"
                    :routeTo="'officialEvent'" />
</template>
<script lang="ts">
import TagDateNavBar from '@/components/tools/common/TagDateNavBar.vue';
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { computed, defineComponent, onMounted, ref, type Ref } from 'vue';
import Api from '@/utils/Api';
import { sectionTips } from '@/assets/static/sectionTips';
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from "@/utils/showEventsByYear";
import { useViewsDataStore } from '@/stores/viewsData';
import { useLoadingStore } from '@/stores/loadingStore';
import type { IBaseEntity } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        TagDateNavBar,
        ComplexGallery
    },
    setup() {
        const allSlides = computed((): IBaseEntity[] => useViewsDataStore().getData('officialEventsData') as IBaseEntity[]);
        const visibleEvents: Ref<IBaseEntity[]> = ref(allSlides.value);
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
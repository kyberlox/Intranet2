<template>
    <div class="page__title mt20">Корпоративная жизнь</div>
    <TagDateNavBar :years="extractYears(allEvents)"
                   :modifiers="'noTag'"
                   @pickYear="(year) => visibleEvents = showEventsByYear(allEvents, year)" />
    <FlexGallery class="mt20"
                 :page=page
                 :slides="visibleEvents"
                 :routeTo="'corpLifeItem'"
                 :onlyImg="true" />
</template>
<script lang="ts">
import { sectionTips } from '@/assets/staticJsons/sectionTips';
import TagDateNavBar from '@/components/TagDateNavBar.vue';
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import Api from '@/utils/Api';
import { defineComponent, ref, onMounted, computed, type ComputedRef, type Ref } from "vue";
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from "@/utils/showEventsByYear";
import { useViewsDataStore } from '@/stores/viewsData';
import { useLoadingStore } from '@/stores/loadingStore';
import type { ICorpLife } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        TagDateNavBar,
        FlexGallery
    },
    setup() {
        const allEvents: ComputedRef<ICorpLife[]> = computed(() => useViewsDataStore().getData('corpLifeData') as ICorpLife[]);
        const visibleEvents: Ref<ICorpLife[]> = ref(allEvents.value);
        onMounted(() => {
            if (allEvents.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Корпоративная_жизнь']}`)
                .then((res) => {
                    useViewsDataStore().setData(res, 'corpLifeData')
                    visibleEvents.value = res;
                })
                .finally(() => {
                    useLoadingStore().setLoadingStatus(false);
                })
        })

        return {
            page: 'officialEvents',
            allEvents,
            showEventsByYear,
            visibleEvents,
            extractYears
        };
    },
});
</script>
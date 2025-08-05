<template>
    <h1 class="page__title mt20">Корпоративная жизнь</h1>
    <TagDateNavBar :years="extractYears(allEvents)"
                   :modifiers="'noTag'"
                   @pickYear="(year: string) => visibleEvents = showEventsByYear(allEvents, year)" />
    <ComplexGallery class="mt10"
                    :page=page
                    :slides="visibleEvents"
                    :routeTo="'corpLifeItem'"
                    :onlyImg="true" />
</template>
<script lang="ts">
import { sectionTips } from '@/assets/static/sectionTips';
import TagDateNavBar from '@/components/tools/common/DateFilter.vue';
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import Api from '@/utils/Api';
import { defineComponent, ref, onMounted, computed, type ComputedRef, type Ref } from "vue";
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
        const allEvents: ComputedRef<IBaseEntity[]> = computed(() => useViewsDataStore().getData('corpLifeData') as IBaseEntity[]);
        const visibleEvents: Ref<IBaseEntity[]> = ref(allEvents.value);
        onMounted(() => {
            if (allEvents.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['КорпоративнаяЖизнь']}`)
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
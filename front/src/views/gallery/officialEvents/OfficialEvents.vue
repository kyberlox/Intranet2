<template>
    <div class="page__title mt20">Официальные события</div>
    <DateFilter v-if="allSlides"
                :buttonText="buttonText"
                :params="extractYears(allSlides)"
                @pickFilter="(year: string) => filterYear(year)" />
    <ComplexGallery v-if="visibleEvents"
                    :key="offEventKey"
                    class="mt20"
                    :page=page
                    :slides="visibleEvents"
                    :routeTo="'officialEvent'" />
</template>
<script lang="ts">
import DateFilter from '@/components/tools/common/DateFilter.vue';
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
        DateFilter,
        ComplexGallery
    },
    setup() {
        const offEventKey = ref(0);
        const allSlides = computed((): IBaseEntity[] => useViewsDataStore().getData('officialEventsData') as IBaseEntity[]);
        const visibleEvents: Ref<IBaseEntity[]> = ref(allSlides.value);
        const buttonText: Ref<string> = ref('Год публикации');

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

        const filterYear = (year: string) => {
            if (!year) {
                visibleEvents.value = allSlides.value;
                buttonText.value = 'Год публикации';
            }
            else {
                buttonText.value = year;
                visibleEvents.value = showEventsByYear(allSlides.value, year);
            }
            offEventKey.value++;
        }
        return {
            allSlides,
            page: 'officialEvents',
            filterYear,
            extractYears,
            visibleEvents,
            buttonText,
            offEventKey,
            showEventsByYear
        };
    },
});
</script>
<template>
<div class="page__title mt20">Фильмы творческого объединения ЭМК</div>
<button @click="showFilter = !showFilter"
        class="btn dropdown-toggle tagDateNavBar__dropdown-toggle">
    Год публикации
</button>
<DateFilter v-if="allSlides && showFilter"
            :buttonText="buttonText"
            :params="extractYears(allSlides)"
            @pickFilter="(year: string) => filterYear(year)" />
<ComplexGallery v-if="visibleEvents"
                :key="offEventKey"
                class="mt20"
                :page=page
                :slides="visibleEvents"
                :routeTo="'filmEmk'" />
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
import type { IBaseEntity } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        DateFilter,
        ComplexGallery
    },
    setup() {
        const offEventKey = ref(0);
        const allSlides = computed((): IBaseEntity[] => useViewsDataStore().getData('filmsEmk') as IBaseEntity[]);
        const visibleEvents: Ref<IBaseEntity[]> = ref(allSlides.value);
        const buttonText: Ref<string> = ref('Год публикации');
        const showFilter = ref(false);
        onMounted(() => {
            if (allSlides.value.length) return;
            Api.get(`article/find_by/${sectionTips['фильмыЕмк']}`)
                .then((res) => {
                    useViewsDataStore().setData(res, 'filmsEmk');
                    visibleEvents.value = res;
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
            showFilter.value = false;
        }
        return {
            allSlides,
            page: 'filmsEmk',
            visibleEvents,
            buttonText,
            offEventKey,
            showFilter,
            filterYear,
            extractYears,
            showEventsByYear
        };
    },
});
</script>
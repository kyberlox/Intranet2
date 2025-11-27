<template>
<h1 class="page__title mt20">Корпоративная жизнь</h1>
<button @click="showFilter = !showFilter"
        class="btn btn-light dropdown-toggle tagDateNavBar__dropdown-toggle">
    Год публикации
</button>
<DateFilter v-if="allEvents && showFilter"
            :buttonText="buttonText"
            :params="extractYears(allEvents)"
            @pickFilter="(year: string) => filterYear(year)" />
<ComplexGallery v-if="visibleEvents"
                :key="galleryKey"
                class="mt10"
                :page=page
                :slides="visibleEvents"
                :routeTo="'corpLifeItem'" />
</template>
<script lang="ts">
import { sectionTips } from '@/assets/static/sectionTips';
import DateFilter from '@/components/tools/common/DateFilter.vue';
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import Api from '@/utils/Api';
import { defineComponent, ref, onMounted, computed, type ComputedRef, type Ref } from "vue";
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
        const allEvents: ComputedRef<IBaseEntity[]> = computed(() => useViewsDataStore().getData('corpLifeData') as IBaseEntity[]);
        const visibleEvents: Ref<IBaseEntity[]> = ref(allEvents.value);
        const buttonText: Ref<string> = ref('Год публикации');
        const galleryKey = ref(0);
        const showFilter = ref(false);

        onMounted(() => {
            if (allEvents.value.length) return;
            Api.get(`article/find_by/${sectionTips['КорпоративнаяЖизнь']}`)
                .then((res) => {
                    useViewsDataStore().setData(res, 'corpLifeData')
                    visibleEvents.value = res;
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
            galleryKey.value++;
            showFilter.value = false;
        }

        return {
            page: 'officialEvents',
            allEvents,
            visibleEvents,
            buttonText,
            galleryKey,
            showFilter,
            showEventsByYear,
            filterYear,
            extractYears
        };
    },
});
</script>
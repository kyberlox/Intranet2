<!-- <template>
    <div class="contest__page mt20">
        <div class="page__title">Конкурсы ЭМК</div>
        <div class="page__title__details"
             v-if="title">{{ title }}</div>
        <ContentGallery v-if="formattedSlides"
                        class="mt20"
                        :page=page
                        :modifiers="modifiers"
                        :slide="slide"
                        @callModal="callModal" />
    </div>
    <ZoomModal v-if="slide && slide.images?.length && modalIsOpen == true"
               :activeIndex="activeIndex"
               :image="slide.images"
               @close="modalIsOpen = false" />
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
import { useLoadingStore } from '@/stores/loadingStore';
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
        }

        return {
            page: 'officialEvents',
            allEvents,
            visibleEvents,
            buttonText,
            galleryKey,
            showEventsByYear,
            filterYear,
            extractYears
        };
    },
});
</script> -->
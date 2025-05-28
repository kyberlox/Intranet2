<template>
    <h2 class="page__title mt20">Корпоративные события</h2>
    <TagDateNavBar :years="years"
                   :modifiers="'noTag'"
                   @pickYear="showEventsByYear" />
    <GridGallery v-if="visibleEvents"
                 :gallery="visibleEvents"
                 :routeTo="'corpEvent'" />
</template>

<script lang="ts">
import { defineComponent, onMounted, type Ref, ref } from "vue";
import TagDateNavBar from "@/components/news/TagDateNavBar.vue";
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import type { ICorpEventsItem } from "@/interfaces/INewNews";

export default defineComponent({
    components: { GridGallery, TagDateNavBar },
    props: {
        pageTitle: String,
        id: String
    },

    setup(props) {
        const allEvents = ref<ICorpEventsItem[]>();
        const visibleEvents = ref<ICorpEventsItem[]>();
        const years = ref<String[]>([]);
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Корпоративные_события']}`)
                .then(res => {
                    years.value.length = 0;
                    allEvents.value = res;
                    visibleEvents.value = res;
                    allEvents.value?.map((e) => {
                        if (e.indirect_data?.ACTIVE_FROM) {
                            years.value.push(e.indirect_data?.ACTIVE_FROM)
                        }
                    })
                    const uniqueYears = [...new Set(years.value.map(date => date.split(' ')[0].split('.')[2]))];
                    years.value = uniqueYears;
                })

        })

        const showEventsByYear = (year: string) => {
            visibleEvents.value = [];
            allEvents.value?.map((e) => {
                if (e.indirect_data?.ACTIVE_FROM?.includes(year)) {
                    visibleEvents.value?.push(e);
                }
            })
        }

        return {
            visibleEvents,
            years,
            showEventsByYear
        };
    },
});
</script>

<template>
    <h2 class="page__title mt20">Корпоративные события</h2>
    <TagDateNavBar v-if="allEvents"
                   :years="extractYears(allEvents)"
                   :modifiers="'noTag'"
                   @pickYear="(year) => visibleEvents = showEventsByYear(allEvents, year)" />
    <GridGallery v-if="visibleEvents"
                 :gallery="visibleEvents"
                 :routeTo="'corpEvent'" />
</template>

<script lang="ts">
import { defineComponent, onMounted, type Ref, ref } from "vue";
import TagDateNavBar from "@/components/TagDateNavBar.vue";
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import { extractYears } from "@/utils/extractYearsFromPosts";
import type { ICorpEventsItem } from "@/interfaces/IEntities";
import { showEventsByYear } from "@/utils/showEventsByYear";

export default defineComponent({
    components: { GridGallery, TagDateNavBar },
    props: {
        pageTitle: String,
        id: String
    },

    setup(props) {
        const allEvents = ref<ICorpEventsItem[]>();
        const visibleEvents = ref<ICorpEventsItem[]>();
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Корпоративные_события']}`)
                .then(res => {
                    allEvents.value = res;
                    visibleEvents.value = res;
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

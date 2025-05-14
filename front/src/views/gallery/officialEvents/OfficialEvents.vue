<template>
    <div class="page__title mt20">Официальные события</div>
    <TagDateNavBar :years="extractYears(allSlides)"
                   :modifiers="'noTag'"
                   @pickYear="(year) => visibleEvents = showEventsByYear(allSlides, year)" />
    <FlexGallery v-if="visibleEvents"
                 class="mt20"
                 :page=page
                 :slides="visibleEvents"
                 :routeTo="'officialEvent'" />
</template>
<script lang="ts">
import TagDateNavBar from '@/components/TagDateNavBar.vue';
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { defineComponent, onMounted, ref } from 'vue';
import Api from '@/utils/Api';
import { sectionTips } from '@/assets/staticJsons/sectionTips';
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from "@/utils/showEventsByYear";

export default defineComponent({
    components: {
        TagDateNavBar,
        FlexGallery
    },
    setup() {
        const allSlides = ref([]);
        const visibleEvents = ref([]);
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['офСобытия']}`)
                .then((res) => {
                    allSlides.value = res;
                    visibleEvents.value = res
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
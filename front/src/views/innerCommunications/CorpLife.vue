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
import { getProperty } from "@/utils/fieldChecker";
import Api from '@/utils/Api';
import { defineComponent, ref, type Ref, onMounted } from "vue";
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from "@/utils/showEventsByYear";

export default defineComponent({
    components: {
        TagDateNavBar,
        FlexGallery
    },
    setup() {
        const allEvents = ref([]);
        const visibleEvents = ref([]);
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Корпоративная_жизнь']}`)
                .then((res) => {
                    allEvents.value = res;
                    visibleEvents.value = res;
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
<template>
    <div class="page__title mt20">Корпоративная жизнь</div>
    <TagDateNavBar :years="years"
                   :modifiers="'noTag'"
                   @pickYear="showEventsByYear" />
    <FlexGallery class="mt20"
                 :page=page
                 :slides="visibleEvents"
                 :routeTo="'corpLifeItem'" />
</template>
<script lang="ts">
import { sectionTips } from '@/assets/staticJsons/sectionTips';
import TagDateNavBar from '@/components/news/TagDateNavBar.vue';
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import Api from '@/utils/Api';
import { defineComponent, ref, type Ref, onMounted } from "vue";

export default defineComponent({
    components: {
        TagDateNavBar,
        FlexGallery
    },
    setup() {
        const allEvents = ref([]);
        const visibleEvents = ref([]);
        const years = ref([]);
        onMounted(() => {
            const events = ref();
            Api.get(`article/find_by/${sectionTips['Корпоративная_жизнь']}`)
                .then((res) => {
                    allEvents.value = res;
                    visibleEvents.value = res;
                    res.map((e) => {
                        if (e.indirect_data && e.indirect_data['PROPERTY_666']) {
                            years.value.push(e.indirect_data['PROPERTY_666'][0])
                        }
                    })

                    const uniqueYears = [...new Set(years.value.map(date => date.split(' ')[0].split('.')[2]))];
                    years.value = uniqueYears;
                })
        })

        const showEventsByYear = (year: string) => {
            visibleEvents.value = [];
            allEvents.value?.map((e) => {
                if (e.indirect_data['PROPERTY_666'][0].includes(year)) {
                    visibleEvents.value?.push(e);
                }
            })
        }
        return {
            page: 'officialEvents',
            allEvents,
            years,
            showEventsByYear,
            visibleEvents
        };
    },
});
</script>
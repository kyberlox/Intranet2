<template>
    <div class="page__title mt20">Актуальные новости</div>
    <TagDateNavBar :years="extractYears(allNews)"
                   @pickYear="(year) => visibleNews = showEventsByYear(allNews, year)" />
    <div class="row">
        <GridGallery v-if="visibleNews"
                     :gallery="visibleNews"
                     :type="'postPreview'"
                     :routeTo="'actualArticle'" />
    </div>
</template>
<script lang="ts">
import { sectionTips } from '@/assets/staticJsons/sectionTips';
import TagDateNavBar from '@/components/TagDateNavBar.vue';
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import Api from '@/utils/Api';
import { defineComponent, onMounted, type Ref, ref } from 'vue';
import type { IActualNews } from '@/interfaces/IEntities';
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from '@/utils/showEventsByYear';

export default defineComponent({
    components: {
        TagDateNavBar,
        GridGallery
    },
    setup() {
        const allNews: Ref<IActualNews[]> = ref([]);
        const visibleNews: Ref<IActualNews[]> = ref([]);
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Актуальные новости']}`)
                .then((res) => {
                    visibleNews.value = res;
                    allNews.value = res;
                })
        })
        return {
            allNews,
            visibleNews,
            extractYears,
            showEventsByYear
        };
    },
});
</script>
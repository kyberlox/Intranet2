<template>
    <div class="page__title mt20">Актуальные новости</div>
    <TagDateNavBar :years="extractYears(allNews)"
                   @pickYear="(year) => visibleNews = showEventsByYear(allNews, year)" />
    <div class="row">
        <GridGallery :gallery="visibleNews"
                     :type="'postPreview'"
                     :routeTo="'actualArticle'" />
    </div>
</template>
<script lang="ts">
import { sectionTips } from '@/assets/staticJsons/sectionTips';
import TagDateNavBar from '@/components/TagDateNavBar.vue';
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import Api from '@/utils/Api';
import { defineComponent, onMounted, type Ref, ref, computed, type ComputedRef } from 'vue';
import type { IActualNews } from '@/interfaces/IEntities';
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from '@/utils/showEventsByYear';
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from '@/stores/loadingStore';
// import GridGallerySkeleton from '@/components/tools/gallery/GridGallerySkeleton.vue';

export default defineComponent({
    components: {
        TagDateNavBar,
        GridGallery,
        // GridGallerySkeleton
    },
    setup() {
        const viewsData = useViewsDataStore();
        const allNews: ComputedRef<IActualNews[]> = computed(() => viewsData.getData('actualNewsData') as IActualNews[]);
        const visibleNews: Ref<IActualNews[]> = ref(allNews.value);
        onMounted(() => {
            if (allNews.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Актуальные новости']}`)
                .then((res) => {
                    viewsData.setData(res, 'actualNewsData');
                    visibleNews.value = res;
                })
                .finally(() => {
                    useLoadingStore().setLoadingStatus(false);
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
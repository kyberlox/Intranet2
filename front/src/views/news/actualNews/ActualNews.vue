<template>
    <div class="page__title mt20">Актуальные новости</div>
    <TagDateNavBar :params="extractYears(allNews)"
                   @pickFilter="(x) => filterNews(x)" />
    <div class="row">
        <GridGallery :gallery="visibleNews"
                     :type="'postPreview'"
                     :routeTo="'actualArticle'" />
    </div>
</template>
<script lang="ts">
import { sectionTips } from '@/assets/static/sectionTips';
import TagDateNavBar from '@/components/tools/common/TagDateNavBar.vue';
import GridGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import Api from '@/utils/Api';
import { defineComponent, onMounted, type Ref, ref, computed, type ComputedRef } from 'vue';
import type { IActualNews } from '@/interfaces/IEntities';
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from '@/utils/showEventsByYear';
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from '@/stores/loadingStore';

export default defineComponent({
    components: {
        TagDateNavBar,
        GridGallery,
    },
    setup() {
        const viewsData = useViewsDataStore();
        const allNews: ComputedRef<IActualNews[]> = computed(() => viewsData.getData('actualNewsData') as IActualNews[]);
        const visibleNews: Ref<IActualNews[]> = ref(allNews.value);

        const filterNews = (param) => {
            visibleNews.value = allNews.value;
            visibleNews.value = allNews.value.filter((e) => { return e.date_creation?.includes(param) })
        }
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
            showEventsByYear,
            filterNews
        };
    },
});
</script>
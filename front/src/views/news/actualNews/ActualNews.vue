<template>
    <div class="page__title mt20">Актуальные новости</div>
    <div class="page__filter">
        <TagDateNavBar :params="extractYears(allNews)"
                       @pickFilter="(x) => filterNews(x)" />
        <TagsBlock @pickTag="handleTagPick" />
    </div>
    <div class="row">
        <GridGallery :gallery="visibleNews"
                     :type="'postPreview'"
                     :routeTo="'actualArticle'" />
    </div>
</template>
<script lang="ts">
import { sectionTips } from '@/assets/static/sectionTips';
import TagDateNavBar from '@/components/tools/common/DateFilterBlock.vue';
import GridGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import Api from '@/utils/Api';
import { defineComponent, onMounted, type Ref, ref, computed, type ComputedRef } from 'vue';
import type { INews } from '@/interfaces/IEntities';
import { extractYears } from '@/utils/extractYearsFromPosts';
import { showEventsByYear } from '@/utils/showEventsByYear';
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from '@/stores/loadingStore';
import TagsBlock from '@/components/tools/common/TagsBlock.vue';

export default defineComponent({
    components: {
        TagDateNavBar,
        GridGallery,
        TagsBlock
    },
    setup() {
        const viewsData = useViewsDataStore();
        const allNews: ComputedRef<INews[]> = computed(() => viewsData.getData('actualNewsData') as INews[]);
        const visibleNews: Ref<INews[]> = ref(allNews.value);

        const filterNews = (param: string) => {
            visibleNews.value = allNews.value;
            visibleNews.value = allNews.value.filter((e) => { return e.date_creation?.includes(param) })
        }

        const handleTagPick = (id) => {
            Api.get(`article/get_articles_by_tag_id/${id}`)
                .then((e) => console.log(e))
            // visibleNews.value = data;
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
            filterNews,
            handleTagPick,
        };
    },
});
</script>
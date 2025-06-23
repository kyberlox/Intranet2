<template>
    <h1 class="page__title mt20">Новости организационного развития</h1>
    <div class="row">
        <div class="news__list">
            <GridGallery :gallery="news"
                         :type="'postPreview'"
                         :routeTo="'corpNewsArticle'" />
        </div>
    </div>
</template>
<script lang="ts">
import GridGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import { defineComponent, type Ref, onMounted, computed } from "vue";
import type { IActualNews } from "@/interfaces/IEntities";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData"
import { useLoadingStore } from "@/stores/loadingStore";
export default defineComponent({
    components: {
        GridGallery
    },
    props: {
        id: Number,
    },
    setup() {
        const viewsData = useViewsDataStore();
        const news: Ref<IActualNews[]> = computed(() => viewsData.getData('corpNewsData') as IActualNews[]);

        onMounted(() => {
            if (news.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['НовостиОргРазвития']}`)
                .then((res) => {
                    viewsData.setData(res, 'corpNewsData');
                })
                .finally(() => {
                    useLoadingStore().setLoadingStatus(false);
                })
        })
        return {
            news
        };
    },
});
</script>
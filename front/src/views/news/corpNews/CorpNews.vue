<template>
<h1 class="page__title mt20">Новости организационного развития</h1>
<div class="row">
    <div class="news__list">
        <SampleGallery :gallery="news"
                       :needDate="true"
                       :modifiers="['noLikes']"
                       :type="'interview'"
                       :routeTo="'corpNewsArticle'" />
    </div>
</div>
</template>
<script lang="ts">
import SampleGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import { defineComponent, type Ref, onMounted, computed } from "vue";
import type { INews } from "@/interfaces/IEntities";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData"
export default defineComponent({
    components: {
        SampleGallery
    },
    props: {
        id: Number,
    },
    setup() {
        const viewsData = useViewsDataStore();
        const news: Ref<INews[]> = computed(() => viewsData.getData('corpNewsData') as INews[]);

        onMounted(() => {
            if (news.value.length) return;
            Api.get(`article/find_by/${sectionTips['НовостиОргРазвития']}`)
                .then((res) => {
                    viewsData.setData(res, 'corpNewsData');
                })
        })
        return {
            news
        };
    },
});
</script>
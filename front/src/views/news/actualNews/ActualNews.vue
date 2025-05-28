<template>
    <div class="page__title mt20">Актуальные новости</div>
    <TagDateNavBar />
    <div class="row">
        <GridGallery v-if="news"
                     :gallery="news"
                     :type="'postPreview'"
                     :routeTo="'actualArticle'" />
    </div>
</template>
<script lang="ts">
import { sectionTips } from '@/assets/staticJsons/sectionTips';
import TagDateNavBar from '@/components/news/TagDateNavBar.vue';
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import Api from '@/utils/Api';
import { defineComponent, onMounted, type Ref, ref } from 'vue';
import type { IActualNews } from '@/interfaces/INewNews';

export default defineComponent({
    components: {
        TagDateNavBar,
        GridGallery
    },
    setup() {
        const news: Ref<IActualNews[]> = ref([]);
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Актуальные новости']}`)
                .then((res) => {
                    news.value = res;
                    console.log(news.value);

                })
        })
        return {
            news
        };
    },
});
</script>
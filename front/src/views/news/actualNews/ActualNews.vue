<template>
    <div class="page__title mt20">Актуальные новости</div>
    <TagDateNavBar />
    <div class="row">
        <GridGallery v-if="formattedNews"
                     :gallery="formattedNews"
                     :type="'postPreview'" />
    </div>
</template>
<script lang="ts">
import TagDateNavBar from '@/components/news/TagDateNavBar.vue';
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import { mainPageCards } from "@/assets/staticJsons/mainPage";
import { defineComponent } from 'vue';

export default defineComponent({
    components: {
        TagDateNavBar,
        GridGallery
    },
    setup() {

        const news = mainPageCards.find((e) => e.id == 6);
        console.log(news);
        const formattedNews = news && news.type == 'fullRowBlock' && news.images ? news.images : [];
        return {
            formattedNews
        };
    },
});
</script>
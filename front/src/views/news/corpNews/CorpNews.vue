<template>
    <div class="page__title mt20">Новости организационного развития</div>
    <div class="row">
        <div class="news__list">
            <GridGallery :gallery="news"
                         :type="'postPreview'"
                         :routeTo="'corpNewsArticle'" />
        </div>
    </div>
</template>
<script lang="ts">
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import { defineComponent, type Ref, onMounted, ref } from "vue";
import type { IActualNews } from "@/interfaces/INewNews";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";

export default defineComponent({
    components: {
        GridGallery
    },
    props: {
        id: String,
    },
    setup() {
        const news: Ref<IActualNews[]> = ref([]);
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Новости орг развития']}`)
                .then((res) => {
                    news.value = res;
                })
        })
        return {
            news
        };
    },
});
</script>
<template>
    <h2 class="page__title mt20">Корпоративные события</h2>
    <TagDateNavBar :modifiers="'noTag'" />
    <GridGallery :gallery="posts"
                 :type="'ourPeople'" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import TagDateNavBar from "@/components/news/TagDateNavBar.vue";
import GridGallery from "@/components/tools/gallery/GridGallery.vue";

export default defineComponent({
    components: { GridGallery, TagDateNavBar },
    setup() {
        const posts = [
            {
                id: 1,
                image: "https://portal.emk.ru/upload/iblock/bb6/opwvwb4yznmcf3x6s0hi58xzoi3ml7q1/1_small.jpg",
                title: "«Мы – настоящая команда»: программисты Саша и Игорь о работе в ЭМК",
                reactions: {
                    views: "12",
                    likes: { count: "13", likedByMe: 1 },
                },
                href: "our-people-interview",
            },
        ];

        return {
            posts,
        };
    },
});
</script>

<template>
    <div class="page__wrapper mt20">
        <h2 class="page__title">Блог Директора по маркетингу</h2>
        <div class="row d-flex mt20 blog__articles-wrapper">
            <div class="avatar__wrapper col-sm-3">
                <BlogAvatar :author="blogArticles" />
            </div>
            <div class="blog-list__item-wrapper col-sm-9">
                <div class="blog-list__item"
                     v-for="article in blogArticles.articles"
                     :key="'article' + article.id">
                    <RouterLink :to="{ name: 'CertainBlog', params: { id: article.id, name: blogArticles.href } }"
                                class="blog-list__item-title">{{ article.title }}</RouterLink>
                    <div class="news-like">
                        <span class="blog-date">{{ article.date + " //" + " " }}</span>
                        <Reactions :reactions="article.reactions"
                                   :type="'blog'" />
                    </div>
                    <div class="blog__short__desc">
                        {{ article.description }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { blogArticles } from "@/assets/staticJsons/blogArticles";
import BlogAvatar from "@/components/about/blogs/BlogAvatar.vue";
import Reactions from "@/components/Reactions.vue";
import { defineComponent } from "vue";
export default defineComponent({
    components: { Reactions, BlogAvatar },
    setup() {
        return {
            blogArticles,
        };
    },
});
</script>

<template>
<div class="page__wrapper mt20">
    <div class="row d-flex mt20 blog__articles-wrapper">
        <div class="blog__avatar__wrapper col-sm-3">
            <BlogAvatar :author="targetAuthor"
                        :from="'blogsArticles'"
                        :needLink="true" />
        </div>
        <div class="blog-list__item-wrapper col-sm-9">
            <div class="blog-list__item"
                 v-for="article in blogsArticles"
                 :key="'article' + article.id">
                <div v-if="article.indirect_data">
                    <RouterLink :to="{ name: 'certainBlog', params: { id: article.id, authorId: targetAuthor?.authorId } }"
                                class="blog-list__item-title">
                        {{ article.name }}
                    </RouterLink>
                    <div class="news-like news-like--blog">
                        <span class="blog-date">{{ article.date_creation?.replace('T', ' ') }} //</span>
                        <Reactions v-if="article.reactions"
                                   :id="article.id"
                                   :reactions="article.reactions"
                                   :type="'blog'" />
                    </div>
                    <div class="blog__short__desc"
                         v-if="article?.preview_text">
                        {{ article.preview_text }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import BlogAvatar from "./components/BlogAvatar.vue";
import Reactions from "@/components/tools/common/Reactions.vue";
import { defineComponent, ref, computed } from "vue";
import { useblogDataStore } from "@/stores/blogData";

export default defineComponent({
    components: { Reactions, BlogAvatar },
    props: {
        id: {
            type: String,
            required: true,
        }
    },
    setup(props) {
        const currentArticles = ref([]);
        const targetBlog = ref();
        const blogData = useblogDataStore();

        const targetAuthor = computed(() => blogData.getCurrentAuthor(props.id));

        const blogsArticles = computed(() => blogData.getCurrentArticles(Number(props.id)));

        return {
            blogsArticles,
            blogName: targetAuthor.value?.title,
            currentArticles,
            targetBlog,
            targetAuthor
        };
    }
}
)

</script>

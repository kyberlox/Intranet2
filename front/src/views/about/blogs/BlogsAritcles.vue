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
                 v-for="article in blogsArticles.sort((a, b) => b.id - a.id)"
                 :key="'article' + article.id">
                <div v-if="article.indirect_data">
                    <RouterLink :to="{ name: 'certainBlog', params: { id: article.id, authorId: targetAuthor?.authorId } }"
                                class="blog-list__item-title">
                        {{ article.name }}
                    </RouterLink>
                    <div class="news-like news-like--blog">
                        <Reactions v-if="article.reactions"
                                   :id="article.id"
                                   :reactions="article.reactions"
                                   :date="article.date_creation"
                                   :type="'blog'" />
                    </div>
                    <div v-if="'fio' in article.indirect_data.users && 'manufacture_id' in article.indirect_data"
                         class="news__detail__date">
                        <span> Автор: </span><span class="underline">{{ article.indirect_data.users.fio }}</span>
                    </div>
                    <div class="blog__short__desc"
                         v-if="article?.preview_text"
                         v-html="parseMarkdown(article.preview_text)">
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
import { dateConvert } from "@/utils/dateConvert";
import { parseMarkdown } from "@/utils/parseMarkdown";

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
            targetAuthor,
            dateConvert,
            parseMarkdown,
        };
    }
}
)

</script>

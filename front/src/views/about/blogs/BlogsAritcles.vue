<template>
    <div v-if="blogName && blogs"
         class="page__wrapper mt20">
        <h2 class="page__title">{{ blogName }}</h2>
        <div class="row d-flex mt20 blog__articles-wrapper">
            <div class="avatar__wrapper col-sm-3">
                <BlogAvatar :author="targetBlog"
                            :from="'blogsArticles'" />
            </div>
            <div class="blog-list__item-wrapper col-sm-9">
                <div class="blog-list__item"
                     @click="console.log(article)"
                     v-for="article in blogsArticles"
                     :key="'article' + article.id">
                    <div v-if="article.PROPERTY_451?.authorId == id">
                        <RouterLink :to="{ name: 'CertainBlog', params: { id: article.id, name: 's' } }"
                                    class="blog-list__item-title">{{ article.NAME }}</RouterLink>
                        <div class="news-like news-like--blog">
                            <span class="blog-date">{{ article.date + " //" + " " }}</span>
                            <Reactions v-if="article.reactions"
                                       :reactions="article.reactions"
                                       :type="'blog'" />
                        </div>
                        <div class="blog__short__desc"
                             v-if="article?.PROPERTY_1009?.description">
                            {{ article.PROPERTY_1009.description }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import BlogAvatar from "@/components/about/blogs/BlogAvatar.vue";
import Reactions from "@/components/Reactions.vue";
import Api from "@/utils/Api";
import { defineComponent, ref, onMounted, watchEffect, computed } from "vue";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import { renameKey } from "@/utils/renameKey";
export default defineComponent({
    components: { Reactions, BlogAvatar },
    props: {
        id: {
            type: String,
            required: true,
        }
    },
    setup(props) {
        const blogs = ref([]);
        const blogsArticles = ref([]);
        const blogName = ref();
        const currentArticles = ref([]);
        const targetBlog = ref();
        onMounted(() => {
            Api.get(API_URL + `article/infoblock/${sectionTips['Блоги']}`)
                .then(res => {
                    const transformedData = res.map(item => {
                        const newItem = { ...item };
                        if (newItem.PROPERTY_444) {
                            renameKey(newItem.PROPERTY_444, "authorId");
                        }
                        return newItem;
                    });
                    blogs.value.length = 0;
                    blogs.value = transformedData;
                })

            Api.get(API_URL + `article/infoblock/${sectionTips['Контент_блогов']}`)
                .then((data) => {
                    const transformedData = data.map(item => {
                        const newItem = { ...item };
                        if (newItem.PROPERTY_451) {
                            renameKey(newItem.PROPERTY_451, "authorId");
                        }
                        if (newItem.PROPERTY_1009) {
                            renameKey(newItem.PROPERTY_1009, "description");
                        }
                        return newItem;
                    });
                    blogsArticles.value.length = 0;
                    blogsArticles.value = transformedData;
                })
        })
        watchEffect(() => {
            if (blogs.value && blogs.value.length && blogsArticles.value && blogsArticles.value.length) {
                blogName.value = blogs.value.find(e => e.PROPERTY_444?.authorId == props.id)?.NAME;
                targetBlog.value = blogs.value.find(e => e.PROPERTY_444?.authorId == props.id);
                console.log(targetBlog.value);

            }
        })
        return {
            blogs,
            blogsArticles,
            blogName,
            currentArticles,
            targetBlog
        };
    },
});
</script>

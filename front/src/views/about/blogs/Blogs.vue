<template>
    <div class="blogs-page mt20">
        <h2 class="page__title">Блоги</h2>
        <div class="mb-sm-5 blogs-section">
            <div class="blogs__list">
                <div class="blogs__items">
                    <BlogAuthor v-for="item in mainBlogJson"
                                :key="item.id"
                                :author="item" />
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import BlogAuthor from "@/components/about/blogs/BlogAvatar.vue";
import { mainBlogJson } from "@/assets/staticJsons/mainBlog";
import { defineComponent } from "vue";
export default defineComponent({
    components: {
        BlogAuthor,
    },
    setup() {

        return {
            mainBlogJson,
        };
    },
});
</script>

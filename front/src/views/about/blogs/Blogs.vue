<template>
    <div class="blogs-page mt20">
        <h2 class="page__title">Блоги</h2>
        <div class="mb-sm-5 blogs-section">
            <div class="blogs__list">
                <div class="blogs__items">
                    <BlogAvatar v-if="blogs"
                                v-for="item in blogs"
                                :key="item.ID"
                                :from="'blogs'"
                                :author="item" />
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import BlogAvatar from "@/components/about/blogs/BlogAvatar.vue";
import { defineComponent, ref, onMounted } from "vue";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import Api from "@/utils/Api";
import { renameKey } from "@/utils/renameKey";
export default defineComponent({
    components: {
        BlogAvatar,
    },
    setup() {
        const blogs = ref([]);
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
        })
        return {
            blogs
        };
    },
});
</script>

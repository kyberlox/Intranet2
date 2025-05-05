<template>
    <div class="blogs-page mt20">
        <h2 class="page__title">Блоги</h2>
        <div class="mb-sm-5 blogs-section">
            <div class="blogs__list">
                <div class="blogs__items">
                    <BlogAvatar v-if="authors"
                                v-for="item in authors"
                                :key="item.ID"
                                :from="'blogs'"
                                :author="item" />
                </div>
                <h2 v-if="factoryAuthors"
                    class="page__title mt20">Блоги от предприятий</h2>
                <div class="blogs__items">
                    <BlogAvatar v-if="factoryAuthors"
                                v-for="item in factoryAuthors"
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
import { defineComponent, ref, onMounted, computed, watch } from "vue";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import Api from "@/utils/Api";
import { renameKey } from "@/utils/renameKey";
import { useblogDataStore } from "@/stores/blogData";

export default defineComponent({
    components: {
        BlogAvatar,
    },
    setup() {
        const authors = ref([]);
        const factoryAuthors = ref([]);
        const blogDataStore = useblogDataStore();
        const allAuthors = computed(() => blogDataStore.getAllAuthors);

        watch(allAuthors, () => {
            if (!allAuthors.value.length) return
            allAuthors.value.map((e) => {
                if (e.title == 'Новая техника ЗАО «САЗ»' || e.title == 'Новая техника ЗАО «НПО «Регулятор»') {
                    factoryAuthors.value.push(e);
                } else {
                    authors.value.push(e);
                }
            })
        }, { immediate: true, deep: true })

        return {
            authors,
            factoryAuthors
        };
    },
});
</script>

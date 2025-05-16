<template>
    <div class="blogs-page mt20">
        <h2 class="page__title">Блоги</h2>
        <div class="mb-sm-5 blogs-section">
            <div class="blogs__list">
                <div v-if="authors"
                      class="blogs__items">
                    <BlogAvatar v-for="item in authors"
                                :key="item.id"
                                :from="'blogs'"
                                :author="item" />
                </div>
                <h2 v-if="factoryAuthors"
                    class="page__title mt20">Блоги от предприятий</h2>
                <div v-if="factoryAuthors"
                     class="blogs__items">
                    <BlogAvatar v-for="item in factoryAuthors"
                                :key="item.id"
                                :from="'blogs'"
                                :author="item" />
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import BlogAvatar from "@/components/about/blogs/BlogAvatar.vue";
import { defineComponent, ref, type Ref, computed, watch } from "vue";
import { useblogDataStore } from "@/stores/blogData";
import type { IBlogAuthors } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        BlogAvatar,
    },
    setup() {
        const authors: Ref<IBlogAuthors[]> = ref([]);
        const factoryAuthors: Ref<IBlogAuthors[]> = ref([]);
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

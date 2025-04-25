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
                <h2 class="page__title mt20">Блоги от предприятий</h2>
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
import { defineComponent, ref, onMounted } from "vue";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import Api from "@/utils/Api";
import { renameKey } from "@/utils/renameKey";
import { log } from "node:console";
export default defineComponent({
    components: {
        BlogAvatar,
    },
    setup() {
        const authors = ref([]);
        const factoryAuthors = ref([]);

        onMounted(() => {
            Api.get(API_URL + `article/find_by/${sectionTips['Блоги']}`)
                .then(res => {
                    res.map((e) => {
                        if (e.indirect_data.TITLE) {
                            console.log(e.indirect_data);
                            e.indirect_data.PROPERTY_451 ? renameKey(e.indirect_data.PROPERTY_451, 'authorId') :
                                renameKey(e.indirect_data.PROPERTY_453, 'authorId')
                            const newAuthor = {
                                title: e.indirect_data.TITLE,
                                id: e.indirect_data.ID,
                                authorId: e.indirect_data.PROPERTY_451 ? e.indirect_data.PROPERTY_451.authorId : e.indirect_data.PROPERTY_453.authorId,
                            }
                            if (!authors.value.length || !authors.value.find(e => e.title == newAuthor.title)) {
                                if (newAuthor.title == 'Новая техника ЗАО «САЗ»' || newAuthor.title == 'Новая техника ЗАО «НПО «Регулятор»') {
                                    factoryAuthors.value.push(newAuthor);
                                } else {
                                    authors.value.push(newAuthor);
                                }
                            }

                        }
                    })
                    console.log(authors.value);

                })
        })
        return {
            authors,
            factoryAuthors
        };
    },
});
</script>

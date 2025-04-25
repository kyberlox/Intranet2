<template>
	<div class="page__wrapper mt20">
		<h2 class="page__title">Блог Директора по маркетингу</h2>
		<div class="row d-flex mt20 blog__articles-wrapper">
			<div class="avatar__wrapper col-sm-3">
				<BlogAvatar :author="blogArticles"
							:from="'certainBlog'" />
			</div>
			<div class="blog-list__item-wrapper col-sm-9"
				 v-html="text"></div>
		</div>
	</div>
</template>

<script lang="ts">
import { blogArticles } from "@/assets/staticJsons/blogArticles";
import BlogAvatar from "@/components/about/blogs/BlogAvatar.vue";
import { defineComponent, onMounted, ref } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import { renameKey } from "@/utils/renameKey";
export default defineComponent({
	components: { BlogAvatar },
	setup() {
		const blogs = ref([]);
		onMounted(() => {
			Api.get(API_URL + `article/infoblock/${sectionTips['Блоги']}`)
				.then(res => {
					console.log(res);
				})
			Api.get(API_URL + `article/infoblock/${sectionTips['Контент_блогов']}`)
				.then(res => {
					const transformedData = res.map(item => {
						const newItem = { ...item };
						if (newItem.PROPERTY_457) {
							renameKey(newItem.PROPERTY_457, "content");
						}
						console.log(newItem);

						return newItem;
					});
					blogs.value.length = 0;
					blogs.value = transformedData;
				})
		})
		const text = ``;

		return {
			blogArticles,
			text,
		};
	},
});
</script>

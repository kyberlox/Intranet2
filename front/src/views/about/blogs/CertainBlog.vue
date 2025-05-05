<template>
	<div class="page__wrapper mt20">
		<div class="row d-flex mt20 blog__articles-wrapper">
			<div class="avatar__wrapper col-sm-3">
				<BlogAvatar :author="targetAuthor"
							:from="'blogsArticles'" />
			</div>
			<div v-if="currentArticle"
				 class="col-sm-9">
				<h2>{{ currentArticle.name }}</h2>
				<div class="blog-list__item-wrapper mt20"
					 v-html="currentArticle.content_text"></div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { blogArticles } from "@/assets/staticJsons/blogArticles";
import BlogAvatar from "@/components/about/blogs/BlogAvatar.vue";
import { defineComponent, onMounted, ref, computed } from "vue";
import { useblogDataStore } from "@/stores/blogData";
import Api from "@/utils/Api";
export default defineComponent({
	components: { BlogAvatar },
	props: {
		id: {
			type: String,
			required: true,
		},
		authorId: {
			type: String,
			required: true,
		}
	},
	setup(props) {
		const blogs = ref([]);
		const blogData = useblogDataStore();
		const currentArticle = computed(() => blogData.getBlogById(props.id))
		const targetAuthor = computed(() => blogData.getCurrentAuthor(props.authorId))

		console.log(targetAuthor.value)

		return {
			blogArticles,
			targetAuthor,
			currentArticle
		};
	},
});
</script>

<template>
	<div class="page__wrapper mt20">
		<div class="row d-flex mt20 blog__articles-wrapper">
			<div class="avatar__wrapper col-sm-3">
				<BlogAvatar :author="targetAuthor"
							:from="'blogsArticles'" />
			</div>
			<div v-if="currentArticle && 'name' in currentArticle"
				 class="col-sm-9">
				<h2>{{ currentArticle.name }}</h2>
				<div class=" mt20"
					 v-html="currentArticle.content_text ?? parseMarkdown(getProperty(currentArticle, 'PROPERTY_1239'))">
				</div>
				<div v-if="getProperty(currentArticle, 'PROPERTY_1222')"
					 class="blog-list__video__wrapper">
					<iframe style="width: 100%; min-height: 480px;"
							id="you-player"
							:src="getProperty(currentArticle, 'PROPERTY_1222')"
							title="YouTube video player"
							frameborder="0"
							allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
							allowfullscreen></iframe>
				</div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import BlogAvatar from "@/components/about/blogs/BlogAvatar.vue";
import { defineComponent, computed } from "vue";
import { useblogDataStore } from "@/stores/blogData";
import { parseMarkdown } from "@/utils/useMarkdown";
import { getProperty } from "@/utils/getPropertyFirstPos";
export default defineComponent({
	components: { BlogAvatar },
	props: {
		id: {
			type: String,
			required: true
		},
		authorId: {
			type: String,
			required: true,
		},
	},
	setup(props) {
		const blogData = useblogDataStore();
		const currentArticle = computed(() => blogData.getBlogById(props.id));
		const targetAuthor = computed(() => blogData.getCurrentAuthor(props.authorId))

		return {
			targetAuthor,
			currentArticle,
			parseMarkdown,
			getProperty
		};
	},
});
</script>

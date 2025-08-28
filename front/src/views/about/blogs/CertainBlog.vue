<template>
	<div class="page__wrapper mt20">
		<div class="row d-flex mt20 blog__articles-wrapper">
			<div class="avatar__wrapper col-sm-4">
				<BlogAvatar :author="targetAuthor"
							:from="'blogsArticles'"
							:needLink="true" />
			</div>
			<div v-if="currentArticle && 'name' in currentArticle"
				 class="col-sm-8">
				<h2>{{ currentArticle.name }}</h2>
				<div v-if="currentArticle.content_text"
					 class="mt20"
					 v-html="parseMarkdown(currentArticle.content_text)">
				</div>
				<div v-if="(currentArticle.indirect_data?.youtube_link)"
					 class="blog-list__video__wrapper">
					<iframe style="width: 100%; min-height: 480px;"
							id="you-player"
							:src="currentArticle.indirect_data?.youtube_link"
							title="YouTube video player"
							allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
							allowfullscreen></iframe>
				</div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import BlogAvatar from "./components/BlogAvatar.vue";
import { defineComponent, computed } from "vue";
import { useblogDataStore } from "@/stores/blogData";
import { parseMarkdown } from "@/utils/parseMarkdown";
export default defineComponent({
	components: { BlogAvatar },
	props: {
		id: {
			type: String,
		},
		authorId: {
			type: String,
			required: true,
		},
		previewPost: {
			type: Object,
		}
	},
	setup(props) {
		const blogData = useblogDataStore();

		const currentArticle = computed(() => props.id ? blogData.getBlogById(props.id) : props.previewPost);
		const targetAuthor = computed(() => blogData.getCurrentAuthor(props.authorId));

		return {
			targetAuthor,
			currentArticle,
			parseMarkdown,
		};
	},
});
</script>

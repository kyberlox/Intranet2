<template>
    <PostInner v-if="currentPost"
               :post="currentPost" />
</template>
<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import Api from "@/utils/Api";
import PostInner from "@/components/PostInner.vue";
import type { IPost } from "@/interfaces/IFeedPost";

export default defineComponent({
    components: {
        PostInner,
    },
    props: {
        id: {
            type: String,
            required: true,
        },
    },
    setup(props) {
        const currentPost = ref<IPost>();
        onMounted(() => {
            Api.get(API_URL + `article/find_by_ID/${props.id}`)
                .then(res => {
                    currentPost.value = res;
                    if (!currentPost.value) return;
                    if (!res.embedVideos || !res.nativeVideos) return;
                    currentPost.value.videos = res.embedVideos.concat(res.nativeVideos);
                })
        })
        return {
            currentPost
        };
    },
});
</script>

<template>
    <PostInner :id="id" />
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import PostInner from "@/components/PostInner.vue";
import Api from "@/utils/Api";
import type { IActualNews } from "@/interfaces/INewNews";

export default defineComponent({
    name: "NewsPreview",
    props: {
        id: {
            type: String,
            required: true,
        }
    },
    components: {
        PostInner
    },
    setup(props){
        const currentPost = ref<IActualNews>();
        onMounted(()=>{
            console.log(props.id)
            Api.get(`article/find_by_ID/${props.id}`)
            .then((res)=>{
                currentPost.value = res;
            })
        })
        return{
            currentPost
        }
    }
})
</script>
<template>
    <PostInner :id="id" />
</template>
<script lang="ts">
import { defineComponent } from "vue";
import PostInner from "@/components/tools/common/PostInner.vue";

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
        return {

        };
    },
});
</script>

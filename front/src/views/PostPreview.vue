<template>
    <div class="excursions__training__page mt20">
        <div v-if="pageTitle"
             class="page__title">{{ pageTitle }}</div>
        <PostInner :id="String(id)" />
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import PostInner from "@/components/PostInner.vue";

export default defineComponent({
    name: "PostPreview",
    props: {
        id: {
            type: String,
            required: true,
        },
        pageTitle: {
            type: String,
        }
    },
    components: {
        PostInner
    },
    setup(props) {
        return {
        }
    }
})
</script>
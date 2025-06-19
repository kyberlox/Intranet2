<template>
    <div class="excursions__training__page mt20">
        <div v-if="pageTitle"
             class="page__title">{{ pageTitle }}</div>
        <PostInner :id="String(id)"
                   :type="type" />
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import PostInner from "@/components/tools/common/PostInner.vue";

export default defineComponent({
    name: "PostPreview",
    props: {
        id: {
            type: String,
            required: true,
        },
        pageTitle: {
            type: String,
        },
        type: {
            type: String,
            default: 'default'
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
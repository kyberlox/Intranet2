<template>
    <div class="excursions__training__page mt20">
        <div v-if="pageTitle"
             class="page__title">{{ pageTitle }}</div>
        <PostInner :id="id == undefined ? undefined : String(id)"
                   :type="type"
                   :previewElement="pageTitle == 'Экскурсии' ? excursions : null" />
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import PostInner from "@/components/tools/common/PostInner.vue";
import { excursions } from "@/assets/static/trainingCenterData";

export default defineComponent({
    name: "PostPreview",
    props: {
        id: {
            type: String || undefined,
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
    setup() {
        return {
            excursions
        }
    }
})
</script>
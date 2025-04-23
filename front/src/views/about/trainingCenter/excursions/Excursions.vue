<template>
    <div class="excursions__training__page mt20">
        <div class="page__title">Экскурсии</div>
        <PostInner page="excursions" />
    </div>
</template>

<script lang="ts">
import PostInner from "@/components/PostInner.vue";
import { defineComponent } from "vue";
export default defineComponent({
    components: {
        PostInner,
    },
    setup() {
        return {};
    },
});
</script>

<template>
    <h2 class="page__title mt20">Наши люди</h2>
    <GridGallery :gallery="posts"
                 :type="'ourPeople'" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import { posts } from "@/assets/staticJsons/ourPeoplePost";
export default defineComponent({
    components: { GridGallery },
    setup() {
        return {
            posts,
        };
    },
});
</script>

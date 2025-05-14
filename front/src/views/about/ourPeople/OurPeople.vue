<template>
    <h2 class="page__title mt20">Наши люди</h2>
    <GridGallery v-if="galleryPosts"
                 :gallery="galleryPosts"
                 :type="'ourPeople'" />
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";

export default defineComponent({
    components: { GridGallery },
    setup() {
        const galleryPosts = ref();
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Наши люди']}`)
                .then((data) => {
                    galleryPosts.value = data
                });
        })
        return {
            galleryPosts
        };
    },
});
</script>

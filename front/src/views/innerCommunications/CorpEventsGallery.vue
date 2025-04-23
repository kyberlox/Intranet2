<template>
    <div class="page__title mt20">Корпоративная жизнь</div>
    <TagDateNavBar :modifiers="'noTag'" />
    <FlexGallery class="mt20"
                 :page=page
                 :slides="slides" />
</template>
<script lang="ts">
import TagDateNavBar from '@/components/news/TagDateNavBar.vue';
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { defineComponent } from "vue";
import { slides } from '@/assets/staticJsons/corpEventsSlides';

export default defineComponent({
    components: {
        TagDateNavBar,
        FlexGallery
    },
    setup() {
        return {
            slides,
            page: 'officialEvents'
        };
    },
});
</script>
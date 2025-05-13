<template>
    <div class="page__title mt20">Официальные события</div>
    <TagDateNavBar :modifiers="'noTag'" />
    <FlexGallery class="mt20"
                 :page=page
                 :slides="slides" />
</template>
<script lang="ts">
import TagDateNavBar from '@/components/news/TagDateNavBar.vue';
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { defineComponent } from 'vue';
import { officialEventSlides } from '@/assets/staticJsons/officialEventsSlides';

export default defineComponent({
    components: {
        TagDateNavBar,
        FlexGallery
    },
    setup() {
        const slides = officialEventSlides;

        return {
            slides,
            page: 'officialEvents'
        };
    },
});
</script>
<template>
    <div class="page__title mt20">Предложения партнеров</div>
    <FlexGallery class="mt20"
                 :page=page
                 :slides="slides" />
</template>
<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { defineComponent } from "vue";
import { slides } from '@/assets/staticJsons/corpEventsSlides';

export default defineComponent({
    components: {
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
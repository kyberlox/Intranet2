<template>
    <div class="experience__page mt20">
        <div class="page__title">Референсы и опыт поставок </div>
        <FlexGallery :page=page
                     :slides="slides"
                     :title="typeof title == 'string' ? title : ''"
                     :modifiers="['noFullWidthImg']" />
    </div>
</template>

<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { useRoute } from "vue-router";
import { defineComponent, ref } from "vue";
import { expTypeSlides } from "@/assets/staticJsons/expieriencePage";
export default defineComponent({
    components: {
        FlexGallery,
    },

    setup() {
        const route = useRoute();
        const slides = expTypeSlides;
        const title = ref(route.params.title)

        return {
            slides,
            page: "experienceTypes",
            title
        };
    },
});
</script>

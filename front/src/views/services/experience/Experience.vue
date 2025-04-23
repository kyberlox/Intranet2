<template>
    <div class="experience__page mt20">
        <div class="page__title">Референсы и опыт поставок </div>
        <FlexGallery :page=page
                     :slides="slides"
                     :modifiers="['noFullWidthImg']" />
    </div>
</template>

<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { defineComponent } from "vue";
import { slides } from "@/assets/staticJsons/expieriencePage";
export default defineComponent({
    components: {
        FlexGallery,
    },
    setup() {

        return {
            slides,
            page: "experience"
        };
    },
});
</script>

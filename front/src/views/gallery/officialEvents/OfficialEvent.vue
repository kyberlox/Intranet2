<template>
    <div class="experience__page mt20">
        <div class="page__title">Официальные события</div>
        <div class="page__title__details">{{ title }}</div>
        <FlexGallery class="mt20"
                     :page=page
                     :modifiers="modifiers"
                     :slides="formattedSlides" />
    </div>
</template>

<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { officialEventSlide } from "@/assets/staticJsons/officialEventsSlides";
import { defineComponent, computed } from "vue";
import type { INewsSlide } from "@/interfaces/INewsSlide";

export default defineComponent({
    components: {
        FlexGallery,
    },
    setup() {
        const slides = officialEventSlide

        const formattedSlides = computed(() => {
            return slides.slides.map((imgUrl: string) => {
                return {
                    img: imgUrl
                } as INewsSlide;
            });
        });
        return {
            title: slides.title,
            formattedSlides,
            page: 'officialEvent',
            modifiers: ['noRoute']
        };
    },
});
</script>
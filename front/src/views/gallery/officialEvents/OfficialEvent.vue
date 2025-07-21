<template>
    <div class="experience__page mt20">
        <div class="page__title">Официальные события</div>
        <div class="page__title__details">{{ title }}</div>
        <ComplexGallery class="mt20"
                        :page=page
                        :modifiers="modifiers"
                        :slides="formattedSlides" />
    </div>
</template>

<script lang="ts">
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { defineComponent, computed, type Ref, ref } from "vue";
import type { IOfficialEvents } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        ComplexGallery,
    },
    setup() {
        const slides: Ref<IOfficialEvents[]> = ref([]);

        const formattedSlides = computed(() => {
            return ''
        });
        return {
            title: slides.value.title,
            formattedSlides,
            page: 'officialEvent',
            modifiers: ['noRoute']
        };
    },
});
</script>
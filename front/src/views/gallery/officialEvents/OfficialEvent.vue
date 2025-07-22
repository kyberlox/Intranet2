<template>
    <div class="experience__page mt20">
        <div class="page__title">Официальные события</div>
        <div class="page__title__details"
             v-if="title">{{ title }}</div>
        <ComplexGallery v-if="formattedSlides"
                        class="mt20"
                        :page=page
                        :modifiers="modifiers"
                        :slides="formattedSlides" />
    </div>
</template>

<script lang="ts">
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { defineComponent, type Ref, ref, onMounted } from "vue";
import type { IBaseEntity } from "@/interfaces/IEntities";
import Api from "@/utils/Api";

export default defineComponent({
    components: {
        ComplexGallery,
    },
    props: {
        id: {
            type: String,
            required: true
        }
    },
    setup(props) {
        const slides: Ref<IBaseEntity | null> = ref(null);
        const formattedSlides = ref();

        onMounted(() => {
            Api.get(`article/find_by_ID/${props.id}`)
                .then((data) => {
                    formattedSlides.value.images = data.images;
                    formattedSlides.value.id = data.id
                })
        })

        return {
            title: slides.value?.name,
            formattedSlides,
            page: 'officialEvent',
            modifiers: ['noRoute']
        };
    },
});
</script>

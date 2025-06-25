<template>
    <div class="flexGallery__card__buttons">
        <RouterLink v-if="slide.indirect_data?.reportages"
                    :to="uniqueRoutesHandle(routeTo, slide, null, 'factoryReports')"
                    class="primary-button primary-button--rounder">Репортажи</RouterLink>
        <RouterLink v-if="slide.indirect_data?.tours"
                    :to="uniqueRoutesHandle(routeTo, slide, null, 'factoryTours')"
                    class="primary-button primary-button--rounder">3D-Туры</RouterLink>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";
import { uniqueRoutesHandle } from "@/router/uniqueRoutesHandle";
import type { IUnionEntities } from "@/interfaces/IEntities";

export default defineComponent({
    name: 'ComplexGalleryCardBasic',
    props: {
        slide: {
            type: Object as PropType<IUnionEntities>,
            required: true
        },
        routeTo: {
            type: String,
            default: undefined
        },
    },
    setup() {
        return {
            uniqueRoutesHandle,
        }
    }
})
</script>

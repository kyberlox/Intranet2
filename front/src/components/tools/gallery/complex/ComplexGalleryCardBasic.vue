<template>
    <RouterLink class="flexGallery__card"
                :to="uniqueRoutesHandle(routeTo, slide)">
        <div class="flexGallery__card__img-wrapper"
             :class="{ 'flexGallery__card__img-wrapper--noFullWidthImg': modifiers.includes('noFullWidthImg') }">
            <div class="flexGallery__card__img"
                 v-lazy-load="slide.preview_file_url ?? slide.photo_file_url">
            </div>
        </div>
        <div v-if="slide.name"
             class="flexGallery__card__title flexGallery__card__title--text-date">
            <span v-if="getProperty(slide as IAfishaItem, 'PROPERTY_375')"> {{ setCardDate(slide) }}</span>
            <span>{{ slide.name }}</span>
        </div>
        <div class="flexGallery__card__buttons"
             v-if="modifiers.includes('buttons')">
            <RouterLink v-if="slide.indirect_data?.reports.length"
                        :to="uniqueRoutesHandle(routeTo, slide, null, 'factoryReports')"
                        class="primary-button primary-button--rounder">Репортажи</RouterLink>
            <RouterLink v-if="slide.indirect_data?.tours.length"
                        :to="uniqueRoutesHandle(routeTo, slide, null, 'factoryTours')"
                        class="primary-button primary-button--rounder">3D-Туры</RouterLink>
        </div>
    </RouterLink>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";
import { getProperty } from "@/utils/getPropertyFirstPos";
import { uniqueRoutesHandle } from "@/router/uniqueRoutesHandle";
import type { IAfishaItem, IUnionEntities } from "@/interfaces/IEntities";

export default defineComponent({
    name: 'ComplexGalleryCardBasic',
    props: {
        slide: {
            type: Object as PropType<IUnionEntities>,
            required: true
        },
        modifiers: {
            type: Array as PropType<string[]>,
            default: () => []
        },
        routeTo: {
            type: String,
            default: undefined
        },
        setCardDate: {
            type: Function as PropType<(slide: IUnionEntities) => string>,
            required: true
        }
    },
    setup() {
        return {
            uniqueRoutesHandle,
            getProperty,
        }
    }
})
</script>

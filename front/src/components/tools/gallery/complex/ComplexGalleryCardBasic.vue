<template>
<RouterLink class="flexGallery__card"
            :to="uniqueRoutesHandle(routeTo, slide)">
    <div class="flexGallery__card__img-wrapper"
         :class="{ 'flexGallery__card__img-wrapper--noFullWidthImg': modifiers.includes('noFullWidthImg') }">
        <div class="flexGallery__card__img"
             :key="`${slide.id}-${isDark}`"
             @mouseenter="console.log(getPreview(slide))"
             v-lazy-load="getPreview(slide)">
        </div>
    </div>
    <div v-if="slide.name"
         class="flexGallery__card__title flexGallery__card__title--text-date">
        <span> {{ checkCardDate(slide) }}</span>
        <span>{{ slide.name }}</span>
    </div>
    <div class="flexGallery__card__buttons"
         v-if="modifiers.includes('buttons')">
        <RouterLink v-if="slide.indirect_data?.reports?.length"
                    :to="uniqueRoutesHandle(routeTo, slide, null, 'factoryReports')"
                    class="primary-button primary-button--rounder">Репортажи</RouterLink>
        <RouterLink v-if="slide.indirect_data?.tours?.length"
                    :to="uniqueRoutesHandle(routeTo, slide, null, 'factoryTours')"
                    class="primary-button primary-button--rounder">3D-Туры</RouterLink>
    </div>
</RouterLink>
</template>

<script lang="ts">
import { defineComponent, type PropType, computed } from "vue";
import { uniqueRoutesHandle } from "@/router/uniqueRoutesHandle";
import type { IFactoryDataTours, IFactoryDataReports, IBaseEntity } from "@/interfaces/IEntities";
import { useStyleModeStore } from "@/stores/styleMode";

interface IComplexGalleryCardBasic extends IBaseEntity {
    indirect_data?: {
        reports?: IFactoryDataReports[],
        tours?: IFactoryDataTours[],
        href?: string,
        date_from?: string,
        date_to?: string
    },
}

export default defineComponent({
    name: 'ComplexGalleryCardBasic',
    props: {
        slide: {
            type: Object as PropType<IComplexGalleryCardBasic>,
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
    },
    setup() {
        const isDark = computed(() => useStyleModeStore().getDarkMode);
        const checkCardDate = (slide: IComplexGalleryCardBasic) => {
            if (!slide.indirect_data?.date_from) return;
            if (slide.indirect_data.date_to && slide.indirect_data.date_to !== slide.indirect_data.date_from) {
                return `${slide.indirect_data.date_from} - ${slide.indirect_data.date_to}`
            }
            else return slide.indirect_data.date_from
        }

        const getPreview = (slide: IComplexGalleryCardBasic) => {
            if ((slide.id == 6178 || slide.id == 6179) && isDark.value) {
                console.log(slide.preview_file_url?.replace('.png', '_dark.png'));

                return slide.preview_file_url?.replace('.png', '_dark.png')
            }
            else {
                console.log(slide.preview_file_url);
                return slide.preview_file_url ?? slide.photo_file_url
            }
        }

        return {
            uniqueRoutesHandle,
            checkCardDate,
            getPreview,
            isDark
        }
    }
})
</script>

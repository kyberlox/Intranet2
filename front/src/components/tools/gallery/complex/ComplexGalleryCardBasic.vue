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
import { computed, defineComponent, type PropType } from "vue";
import { uniqueRoutesHandle } from "@/router/uniqueRoutesHandle";
import type { IFactoryDataTours, IFactoryDataReports, IBaseEntity } from "@/interfaces/IEntities";

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
    setup(props) {

        const checkCardDate = (slide: IComplexGalleryCardBasic) => {
            if (!slide.indirect_data?.date_from) return;
            if (slide.indirect_data.date_to && slide.indirect_data.date_to! === slide.indirect_data.date_from) {
                return `${slide.indirect_data.date_from} - ${slide.indirect_data.date_to}`
            }
            else return slide.indirect_data.date_from
        }

        return {
            imageUrl: computed(() => props.slide.preview_file_url ?? props.slide.photo_file_url),
            uniqueRoutesHandle,
            checkCardDate,
        }
    }
})
</script>

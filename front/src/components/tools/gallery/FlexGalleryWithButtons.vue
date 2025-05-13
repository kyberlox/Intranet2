<template>
    <div class="flexGallery">
        <div class="flexGallery__card flexGallery__card--with-buttons"
             v-for="(slide, index) in slides"
             :key="index">
            <div class="flexGallery__card__img-wrapper flexGallery__card__img-wrapper--noFullWidthImg">
                <div class="flexGallery__card__img"
                     :style="{ backgroundImage: `url(${slide.img})` }">
                </div>
            </div>
            <div class="flexGallery__card__title">{{ slide.title }}</div>
            <div class="flexGallery__card__buttons">
                <RouterLink v-if="slide.reportages"
                            :to="{ name: slide.reportsHref, params: { title: slide.hrefTitle } }"
                            class="flexGallery__card__buttons__button">Репортажи</RouterLink>
                <RouterLink v-if="slide.tours"
                            :to="{ name: slide.toursHref, params: { title: slide.hrefTitle } }"
                            class="flexGallery__card__buttons__button">3D-Туры</RouterLink>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import type { INewsSlide } from '@/interfaces/INewsSlide'
import { defineComponent } from 'vue'
import type { PropType } from 'vue'
export default defineComponent({
    name: 'FlexGallery',
    props: {
        slides: {
            type: Array as PropType<INewsSlide[]>,
        },
        page: {
            type: String,
        },
        title: {
            type: String,
        }
    },

    setup(props) {
        const checkRouteTo = (slide: INewsSlide) => {
            if (props.page === 'experience') {
                return { name: 'experienceTypes', params: { title: slide.href } }
            }
            else if (props.page === 'experienceTypes') {
                return { name: 'experienceType', params: { title: props.title, id: slide.id } }
            }
        }

        return {
            checkRouteTo
        }
    }
})
</script>
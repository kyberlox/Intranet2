<template>
    <div v-if="slide"
         class="col-12 col-md-6 col-lg-6 col-xl-4 col-xxl-3">
        <div class="section__image__list__item"
             :style="{ backgroundImage: `url('https://placehold.co/360x533')` }">
            <div class="section__image__list__item__banner">
                <div class="section__image__list__item__logo">
                    <img src="/src/assets/imgs/emkLogo.webp"
                         alt="ЭМК"
                         title="ЭМК" />
                </div>
                <span class="section__image__list__item__banner__inner"
                      v-if="place !== 'inner'">
                    <span class="section__image__list__item__category">
                        {{ getProperty(slide, "PROPERTY_344") }}
                    </span>
                    <h3 v-if="slide.indirect_data && slide.indirect_data.NAME"
                        class="section__image__list__item__title">{{ slide.indirect_data.NAME }}</h3>
                    <RouterLink :to="{ name: routeTo, params: { id: slide.id } }"
                                class="section__image__list__item__link">
                        Читать
                    </RouterLink>
                </span>
            </div>
        </div>
        <div class="section__image__list__item__subtitle__wrapper">
            <div class="section__image__list__item__subtitle vertical-title">{{ slide.name }}</div>
            <div class="section__image__list__item__subtitle vertical-subtitle">
                Организатор: {{ getProperty(slide, "PROPERTY_435") }}
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { getProperty } from '@/utils/getPropertyFirstPos';
import type { ISafetyTechnicsSlide } from '@/interfaces/IEntities';

export default defineComponent({
    props: {
        slide: {
            type: Object as PropType<ISafetyTechnicsSlide>,
            required: true,
        },
        place: {
            default: "outer",
            type: String,
        },
        routeTo: {
            type: String,
        }
    },
    setup() {
        return {
            getProperty
        };
    },
});
</script>

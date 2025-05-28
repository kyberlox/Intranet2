<template>
    <div class="col-12 col-md-6 col-lg-6 col-xl-4 col-xxl-3">
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
                    <span class="section__image__list__item__category">{{
                        slide.indirect_data["PROPERTY_344"][0] }}</span>
                    <h3 class="section__image__list__item__title">{{ slide.indirect_data.name }}</h3>
                    <RouterLink :to="{ name: routeTo, params: { id: slide.id } }"
                                class="section__image__list__item__link">Читать</RouterLink>
                </span>
            </div>
        </div>
        <div class="section__image__list__item__subtitle vertical-title">{{ slide.name }}</div>
        <div class="section__image__list__item__subtitle vertical-subtitle">Организатор: {{
            slide.indirect_data["PROPERTY_435"][0] }}</div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
    props: {
        slide: {
            type: Object,
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
        return {};
    },
});
</script>

<template>
    <div class="col-12 col-md-6 col-lg-6 col-xl-4 col-xxl-3">
        <div class="section__image__list__item">
            <div class="section__image__list__item__banner"
                 :style="`background: url('${slide.image}'); 50% no-repeat; background-size: cover`">
                <div class="section__image__list__item__logo">
                    <img src="/src/assets/imgs/emkLogo.webp"
                         alt="ЭМК"
                         title="ЭМК" />
                </div>
                <span class="section__image__list__item__banner__inner"
                      v-if="place !== 'inner'">
                    <span class="section__image__list__item__category">{{ slide.header }}</span>
                    <h3 class="section__image__list__item__title">{{ slide.title }}</h3>
                    <RouterLink :to="{ name: slide.href }"
                                class="section__image__list__item__link">Читать</RouterLink>
                </span>
            </div>
            <div class="section__image__list__item__subtitle vertical-title">{{ slide.subtitle }}</div>
            <div class="section__image__list__item__subtitle vertical-subtitle">{{ slide.description }}</div>
        </div>
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
        }
    },
    setup() {
        return {};
    },
});
</script>

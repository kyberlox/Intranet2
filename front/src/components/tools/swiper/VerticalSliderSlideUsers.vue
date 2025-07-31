<template>
    <RouterLink :to="{ name: 'userPage', params: { id: slide?.id } }"
                class="birthday__slide__grid">
        <div class="birthday__slide__image"
             :style="{ backgroundImage: `url('${slide?.image}')` }">
        </div>
        <div class="birthday__slide__info">
            <div class="birthday__page__swiper__slide__title">{{ slide?.user_fio }}</div>
            <div class="birthday__page__swiper__slide__subtitle">{{ slide?.position }}</div>
            <div class="birthday__page__swiper__slide__departments">
                <div class="birthday__page__swiper__slide__department"
                     v-for="(dep, index) in slide?.department"
                     :key="'dep' + index">
                    {{ dep }}
                </div>
            </div>
        </div>
    </RouterLink>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';

interface IBirthdaySlide {
    department: string[],
    id: number,
    image: string,
    position: string,
    user_fio: string
}

export default defineComponent({
    name: 'verticalSliderSlide',
    props: {
        slide: {
            type: Object as PropType<IBirthdaySlide>
        }
    },
    setup() {
        return {
        }
    }
})
</script>
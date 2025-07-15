<template>
    <div class="birthday__slide__grid">
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
    </div>
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
    props: {
        slide: {
            type: Object as PropType<IBirthdaySlide>
        }
    },
    setup(props) {
        console.log(props);
        return {
        }
    }
})
</script>
<style scoped>
.birthday__slide__grid {
    display: grid;
    grid-template-rows: 1fr auto;
    height: 100%;
    min-height: 400px;
}

.birthday__slide__image {
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    min-height: 300px;
}

.birthday__slide__info {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    font-size: 12px;
    padding: 12px;
    background: white;
    min-height: 100px;
    border: 1px solid #e0e0e0;
    border-top: none;
}

.birthday__page__swiper__slide__title {
    font-weight: bold;
}

.birthday__page__swiper__slide__subtitle {
    color: #666;
}
</style>
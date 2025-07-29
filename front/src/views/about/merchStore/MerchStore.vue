<template>
    <div class="mt20">
        <div class="page__title">Магазин мерча</div>
        <div class="merchStore__grid__wrapper">
            <div class="merchStore__grid">
                <RouterLink :to="{ name: 'merchStoreItem', params: { id: item.id } }"
                            class="merchStore__grid__item"
                            v-for="item in storePlug"
                            :key="item.id">
                    <div class="merchStore__grid__item__info">
                        <HoverGallery :images="item.images"
                                      :showIndicators="true" />
                    </div>
                    <div class="merchStore__grid__item__title">
                        {{ item.title }}
                    </div>
                    <div
                         class="merchStore__grid__item__price merchStore__grid__item__info__item__price merchStore__grid__item__info__item">
                        <span class=""> {{ item.price }} </span> эмк-коинов
                    </div>
                </RouterLink>

            </div>
        </div>
    </div>
</template>

<script lang="ts">
import type { Swiper as SwiperType } from 'swiper';
import { Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import { defineComponent, ref } from 'vue';
import HoverGallery from './components/HoverGallery.vue';

export default defineComponent({
    components: {
        HoverGallery
    },
    setup() {

        const storePlug = [
            {
                id: 9,
                title: 'Подушка для самолета',
                images: ['/imgs/merchStore/9pod.png', '/imgs/merchStore/10futb.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 10,
                title: 'Футболка с резиной (черная)',
                images: ['/imgs/merchStore/10futb.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 11,
                title: 'Футболка с резиной (белая)',
                images: ['/imgs/merchStore/11futb.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 12,
                title: 'Худи (черный)',
                images: ['/imgs/merchStore/12hoodie.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 1,
                title: 'Зонт складной (черный)',
                images: ['/imgs/merchStore/1zont.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 2,
                title: 'Внешний аккумулятор',
                images: ['/imgs/merchStore/2zont.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 3,
                title: 'Спортивная сумка',
                images: ['/imgs/merchStore/3sumka.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 4,
                title: 'Панама',
                images: ['/imgs/merchStore/4panama.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 5,
                title: 'Бутылка для воды (стекло)',
                images: ['/imgs/merchStore/5voda.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 6,
                title: 'Бутылка для воды (пластик)',
                images: ['/imgs/merchStore/6voda.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 7,
                title: 'Вечный карандаш',
                images: ['/imgs/merchStore/7karandash.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 8,
                title: 'Сумка',
                images: ['/imgs/merchStore/8sumka.png'],
                price: '1000',
                count: '1'
            },
        ]


        const sliderConfig = {
            modules: [Pagination],
            slidesPerView: 1,
        };

        const swiperInstance = ref<SwiperType | null>(null);

        const swiperOn = (swiper: SwiperType) => {
            swiperInstance.value = swiper;
        }
        return {
            storePlug,
            sliderConfig,
            swiperOn
        }
    }
})
</script>
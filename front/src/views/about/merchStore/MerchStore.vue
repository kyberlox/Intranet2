<template>
<div class="mt20">
    <div class="page__title">Магазин мерча</div>
    <div class="merch-store__grid__wrapper">
        <div class="merch-store__grid">
            <RouterLink :to="{ name: 'merchStoreItem', params: { id: item.id } }"
                        class="merch-store__grid__item"
                        v-for="item in merchItems"
                        :key="item.id">
                <div v-if="item.indirect_data?.images"
                     class="merch-store__grid__item__info">
                    <HoverGallery :images="item.indirect_data?.images as IBXFileType[]"
                                  :showIndicators="true" />
                </div>
                <div class="merch-store__grid__item__title">
                    {{ item.name }}
                </div>
                <div
                     class="merch-store__grid__item__price merch-store__grid__item__info__item__price merch-store__grid__item__info__item">
                    <span class="">
                        {{ item.indirect_data?.price }}
                    </span> эмк-коинов
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
import { defineComponent, onMounted, ref } from 'vue';
import HoverGallery from './components/HoverGallery.vue';
import Api from '@/utils/Api';
import { sectionTips } from '@/assets/static/sectionTips';
import type { IMerch } from '@/interfaces/entities/IMerch';
import type { IBXFileType } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        HoverGallery,
    },
    setup() {
        const storePlug = [
            {
                id: 9,
                title: 'Подушка для самолета',
                images: ['/imgs/merchStore/9pod.png', '/imgs/merchStore/10pod.png'],
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
                id: 6,
                title: 'Бутылка для воды (пластик)',
                images: ['/imgs/merchStore/6voda.png'],
                price: '1000',
                count: '1'
            },
            {
                id: 4,
                title: 'Панама',
                images: ['/imgs/merchStore/4panama.png', '/imgs/merchStore/5panama.png'],
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
                id: 5,
                title: 'Бутылка для воды (стекло)',
                images: ['/imgs/merchStore/5voda.png'],
                price: '1000',
                count: '1'
            },
        ]

        const merchItems = ref<IMerch[]>([]);

        const sliderConfig = {
            modules: [Pagination],
            slidesPerView: 1,
        };

        const swiperInstance = ref<SwiperType | null>(null);
        const swiperOn = (swiper: SwiperType) => {
            swiperInstance.value = swiper;
        }

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['МагазинМерча']}`)
                .then((data) => merchItems.value = data)
        })

        return {
            storePlug,
            sliderConfig,
            merchItems,
            swiperOn
        }
    }
})
</script>

<style>
.hover-gallery__image {
    max-width: 100%;
    object-fit: contain;
    background: whitesmoke;
    border-radius: 20px;
}
</style>
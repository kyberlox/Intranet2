<template>
    <div class="mt20">
        <div class="page__title">Магазин мерча</div>
        <div class="merchStore__grid__wrapper">
            <div class="merchStore__grid">
                <div class="merchStore__grid__item"
                     v-for="item in storePlug"
                     :key="item.id">
                    <div class="merchStore__grid__item__info">
                        <div class="merchStore__grid__item__image"
                             :style="{ backgroundImage: `url(${item.image})` }">
                        </div>
                    </div>
                    <div class="merchStore__grid__item__title">
                        {{ item.title }}
                    </div>
                    <div>
                        <div
                             class="merchStore__grid__item__price merchStore__grid__item__info__item__price merchStore__grid__item__info__item">
                            <span class="count-text"> {{ item.price }} </span> эмк-коинов
                        </div>

                        <div class="merchStore__grid__item__count merchStore__grid__item__info__item">
                            <span class="count-text">{{ item.count }}</span> шт. осталось
                        </div>
                    </div>
                    <div class="merchStore__grid__item__action">
                        <button class="primary-button merchStore__grid__item__button">
                            Оформить
                        </button>
                        <RouterLink :to="{ name: 'merchStoreItem', params: { id: 1 } }"
                                    class="primary-button merchStore__grid__item__button">
                            К товару
                        </RouterLink>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    setup() {
        const storePlug = [
            {
                id: 9,
                title: 'Подушка для самолета',
                image: '/imgs/merchStore/9pod.png',
                price: '1000',
                count: '1'
            },
            {
                id: 10,
                title: 'Футболка с резиной (черная)',
                image: '/imgs/merchStore/10futb.png',
                price: '1000',
                count: '1'
            },
            {
                id: 11,
                title: 'Футболка с резиной (белая)',
                image: '/imgs/merchStore/11futb.png',
                price: '1000',
                count: '1'
            },
            {
                id: 12,
                title: 'Худи (черный)',
                image: '/imgs/merchStore/12hoodie.png',
                price: '1000',
                count: '1'
            },
            {
                id: 1,
                title: 'Зонт складной (черный)',
                image: '/imgs/merchStore/1zont.png',
                price: '1000',
                count: '1'
            },
            {
                id: 2,
                title: 'Внешний аккумулятор',
                image: '/imgs/merchStore/2zont.png',
                price: '1000',
                count: '1'
            },
            {
                id: 3,
                title: 'Спортивная сумка',
                image: '/imgs/merchStore/3sumka.png',
                price: '1000',
                count: '1'
            },
            {
                id: 4,
                title: 'Панама',
                image: '/imgs/merchStore/4panama.png',
                price: '1000',
                count: '1'
            },
            {
                id: 5,
                title: 'Бутылка для воды (стекло)',
                image: '/imgs/merchStore/5voda.png',
                price: '1000',
                count: '1'
            },
            {
                id: 6,
                title: 'Бутылка для воды (пластик)',
                image: '/imgs/merchStore/6voda.png',
                price: '1000',
                count: '1'
            },
            {
                id: 7,
                title: 'Вечный карандаш',
                image: '/imgs/merchStore/7karandash.png',
                price: '1000',
                count: '1'
            },
            {
                id: 8,
                title: 'Сумка',
                image: '/imgs/merchStore/8sumka.png',
                price: '1000',
                count: '1'
            },
        ]
        return {
            storePlug
        }
    }
})
</script>
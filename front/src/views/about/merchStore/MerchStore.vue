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

<style lang="scss" scoped>
.merchStore__title {
    width: 100%;
    background: white;
    padding: 0 10px;
}

.merchStore__grid__wrapper {
    padding: 14px;
}

.merchStore__grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 32px;
    padding: 0;
}

.merchStore__grid__item {
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    cursor: pointer;
    display: flex;
    flex-direction: column;

}

.merchStore__grid__item__title {
    padding: 6px;
    font-size: 18px;
    text-align: center;
    line-height: 1.3;
    position: relative;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.12),
        0 1px 2px rgba(0, 0, 0, 0.08);
    background: var(--emk-brand-color);
    color: white;
    border-radius: 0 0 12px 12px;
}

.merchStore__grid__item__image {
    position: relative;
    width: 100%;
    height: 280px;
    border-radius: 0 12px 0 0;
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    transition: all 0.4s ease;
}

.merchStore__grid__item:hover .merchStore__grid__item__image {
    transform: scale(1.08);
}


.merchStore__grid__item__info {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.merchStore__grid__item__count {
    padding-bottom: 12px;
}

.merchStore__grid__item__info__item {
    text-align: left;
    position: relative;
    margin-left: 8px;
    margin-top: 10px;
}


.merchStore__grid__item:hover .merchStore__grid__item__price span::after {
    color: rgba(255, 255, 255, 0.9);
}

.merchStore__grid__item__action {
    padding: 12px 12px 12px;
    opacity: 1;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: row;
    background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
    align-items: center;
    justify-content: center;
    gap: 20px;
}

.count-text {
    color: var(--emk-brand-color);
}

/* Адаптивность */
@media (max-width: 768px) {
    .merchStore__grid__wrapper {
        padding: 24px 16px;
    }

    .merchStore__grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(219px, 1fr));
        gap: 32px;
        padding: 0;
        margin-top: 20px;
    }

    .merchStore__grid__item__title {
        font-size: 18px;
        padding: 20px 20px 12px;
    }

    .merchStore__grid__item__image {
        height: 240px;
        margin: 0 12px;
        width: calc(100% - 24px);
    }



    .merchStore__grid__item__price span {
        font-size: 20px;
    }
}

@media (max-width: 480px) {
    .merchStore__grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }

    .merchStore__grid__item__image {
        height: 220px;
    }

    .merchStore__grid__item__action {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>

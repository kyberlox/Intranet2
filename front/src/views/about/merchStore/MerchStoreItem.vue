<template>
    <div class="merchStoreItem__wrapper">
        <RouterLink :to="{ name: 'merchStoreItem', params: { id: 1 } }"><button>1 variant</button></RouterLink>
        <RouterLink :to="{ name: 'merchStoreItemTest', params: { id: 1 } }"><button>2 variant</button></RouterLink>
        <div class="merchStoreItem mt20">
            <div class="merchStoreItem__images__wrapper">
                <div class="merchStoreItem__images">
                    <div v-for="(image, index) in merchItemPlug.images"
                         :key="'img' + index"
                         class="merchStoreItem__images__image">
                        <img @click="callModal(index)"
                             :src="image" />
                    </div>
                </div>
            </div>
            <div class="merchStoreItem__info">
                <div class="merchStoreItem__info__category">{{ merchItemPlug.category }}</div>
                <div class="merchStoreItem__info__title">
                    {{ merchItemPlug.title }}
                </div>
                <div class="merchStoreItem__info__description"
                     v-html="merchItemPlug.description">
                </div>
                <div class="merchStoreItem__info__sizes__title">
                    Размер
                </div>
                <div class="merchStoreItem__info__sizes">
                    <div class="merchStoreItem__info__size"
                         v-for="item in merchItemPlug.sizes"
                         :key="'size' + item">
                        {{ item }}
                    </div>
                </div>

                <div class="merchStoreItem__info__price">
                    <span class="count-text"> {{ merchItemPlug.price }}</span> эмк-коинов
                </div>

                <div class="merchStoreItem__info__count">
                    <span class="count-text"> {{ merchItemPlug.count }}</span> шт. осталось
                </div>
                <div class="merchStoreItem__action__wrapper">
                    <div class="merchStoreItem__action__button">
                        Оформить
                    </div>
                </div>
                <!-- <div class="merchStoreItem__info__colors">
                    <div v-for="(color, index) in merchItemPlug.colors"
                         :key="'color' + index"
                         class="merchStoreItem__info__color">
                        {{ color }}
                    </div>
                </div> -->
                <!-- <div class="merchStoreItem__info__material">{{ merchItemPlug.material }}</div> -->

                <ZoomModal v-if="modalIsVisible"
                           :image="merchItemPlug.images"
                           :activeIndex="activeIndex"
                           @close="modalIsVisible = false" />
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import ZoomModal from '@/components/tools/modal/ZoomModal.vue';
import { defineComponent, ref } from 'vue';

export default defineComponent({
    props: {
        id: {
            type: Number,
            default: 1
        },
    },
    components: {
        ZoomModal
    },
    setup() {
        const merchItemPlug = {
            id: 1,
            title: 'Панама',
            price: '1000',
            count: '1',
            images: ['/imgs/merchStore/6voda.png', '/imgs/merchStore/2.png', '/imgs/merchStore/1.png', '/imgs/merchStore/2.png'],
            sizes: ['s', 'm', 'l', 'xl', 'xxl'],
            description: 'Стильная хлопковая панамка с широкими полями для максимальной защиты от солнца. Выполнена из дышащего материала премиум-качества с влагоотводящей подкладкой. Идеально подходит для пляжного отдыха, рыбалки и активного отдыха на природе. Регулируемый размер благодаря внутренней тесьме.',
            category: 'Головные уборы',
            colors: ['оранжевый-черный'],
            material: '100% хлопок',
        }
        const modalIsVisible = ref(false);
        const activeIndex = ref(0);

        const callModal = (index: number) => {
            activeIndex.value = index;
            modalIsVisible.value = true;
        }
        return {
            merchItemPlug,
            modalIsVisible,
            activeIndex,
            callModal
        }
    }
})
</script>

<style lang="scss">
.merchStoreItem {
    display: flex;
    flex-direction: row;
    gap: 24px;

    &__info {
        display: flex;
        flex-direction: column;

        &__category {
            font-size: 14px;
            color: rgba(141, 141, 141, 0.579);
        }

        &__title {
            margin-top: 12px;
            font-size: 75px;
        }

        &__description {
            margin-top: 40px;
            font-size: 16px;
        }

        &__sizes {
            margin-top: 8px;
            display: flex;
            flex-direction: row;
            gap: 24px;

            &__title {
                margin-top: 40px;
            }
        }

        &__size {
            width: 50px;
            height: 50px;
            color: black;
            border: 2px solid rgb(168, 168, 168);
            display: flex;
            align-content: center;
            justify-content: center;
            align-items: center;
            transition: 0.2s all;
            cursor: pointer;

            &:hover {
                border: 2px solid black;
            }

            &--active {
                border: 2px solid black;
            }
        }

        &__price {
            margin-top: 60px;
            font-size: 35px;
        }

        &__count {
            margin-top: 10px;
        }
    }

    &__action {
        &__wrapper {
            margin-top: 20px;
        }

        &__button {
            padding: 29px 0;
            background: black;
            color: white;
            width: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
    }

    &__images {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;

        &__wrapper {}

        &__image {
            height: 100%;

            &:first-child {
                grid-column: 1 / -1;
                // height: 650px;
            }

            &:nth-child(n+2) {
                grid-column: span 1;
            }

            &>img {
                max-width: 100%;
                aspect-ratio: auto;
                /* margin: auto; */
                text-align: center;
                min-width: 100%;
                display: flex;
                height: 100%;
                transition: 0.2s;
                cursor: pointer;

                &:hover {
                    transform: scale(1.05);
                }
            }
        }
    }



    /* Адаптивность для мобильных устройств */
    @media (max-width: 768px) {
        .merchStoreItem__images__wrapper {
            grid-template-columns: 1fr;
            gap: 12px;
        }

        .merchStoreItem__images__wrapper>*:first-child {
            grid-column: 1;
        }
    }
}

.count-text {
    color: var(--emk-brand-color);
}


// 
.merchStoreItem__action {
    &__button {
        padding: 20px 60px;
        background: black;
        color: var(--emk-brand-color);
        border: 1px solid var(--emk-brand-color);
        border-radius: 8px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        transition: color 0.4s ease;
        z-index: 1;

        &::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: var(--emk-brand-color);
            transition: left 0.4s ease;
            z-index: -1;
        }

        &:hover {
            color: white;

            &::before {
                left: 0;
            }
        }
    }
}
</style>
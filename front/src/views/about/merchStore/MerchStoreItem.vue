<template>
<div class="merch-store-item__wrapper">
    <div class="merch-store-item mt20">
        <div class="merch-store-item__images__wrapper">
            <div class="merch-store-item__images__flex-gallery">
                <div v-for="(card, index) in merchItemPlug.images"
                     :key="index"
                     class="merch-store-item__images__flex-gallery__card__wrapper">
                    <div class="merch-store-item__images__flex-gallery__card">
                        <img class="pos-rel"
                             :src="card"
                             @click="setZoomImg(card)" />
                        <ZoomInIcon class="merch-store-item__images__flex-gallery__card__zoom-icon" />
                    </div>
                </div>
            </div>
        </div>
        <div class="merch-store-item__info">
            <div class="merch-store-item__info__category">{{ merchItemPlug.category }}</div>
            <div class="merch-store-item__info__title">
                {{ merchItemPlug.title }}
            </div>
            <div class="merch-store-item__info__description"
                 v-html="merchItemPlug.description">
            </div>
            <div class="merch-store-item__info__sizes__title">
                Размер
            </div>
            <div class="merch-store-item__info__sizes">
                <div class="merch-store-item__info__size"
                     :class="{ 'merch-store-item__info__size--active': item == currentSize }"
                     v-for="item in merchItemPlug.sizes"
                     :key="'size' + item"
                     @click="setCurrentSize(item)">
                    {{ item }}
                </div>
            </div>

            <div class="merch-store-item__info__price">
                <span class="merch-store-item__info__count-text"> {{ merchItemPlug.price }}</span> эмк-коинов
            </div>

            <div class="merch-store-item__info__count">
                <span class="merch-store-item__info__count-text"> {{ merchItemPlug.count }}</span> шт. осталось
            </div>
            <div class="merch-store-item__action__wrapper">
                <div class="merch-store-item__action__button"
                     @click="acceptBuyModalOpen = true">
                    Оформить
                </div>
            </div>
        </div>
    </div>
    <ZoomModal v-if="modalIsOpen == true"
               :image="[activeImage]"
               @close="modalIsOpen = false" />

    <AcceptBuyModal v-if="acceptBuyModalOpen"
                    @closeModal="acceptBuyModalOpen = false"
                    @acceptBuy="acceptBuy" />
</div>
</template>

<script lang="ts">
import ZoomModal from '@/components/tools/modal/ZoomModal.vue';
import { defineComponent, ref } from 'vue';
import ZoomInIcon from "@/assets/icons/merchstore/ZoomInIcon.svg?component"
import AcceptBuyModal from './components/AcceptBuyModal.vue';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';

export default defineComponent({
    components: {
        ZoomModal,
        ZoomInIcon,
        AcceptBuyModal
    },
    props: {
        id: {
            type: Number,
            default: 1
        },
    },
    setup() {
        const merchItemPlug = {
            id: 1,
            title: 'Панама',
            price: '1000',
            count: '1',
            images: ['/imgs/merchStore/2.png', '/imgs/merchStore/1.png'],
            sizes: ['s', 'm', 'l', 'xl', 'xxl'],
            description: 'Стильная хлопковая панамка с широкими полями для максимальной защиты от солнца. Выполнена из дышащего материала премиум-качества с влагоотводящей подкладкой. Идеально подходит для пляжного отдыха, рыбалки и активного отдыха на природе. Регулируемый размер благодаря внутренней тесьме.',
            category: 'Головные уборы',
            colors: ['оранжевый-черный'],
            material: '100% хлопок',
        }

        const activeImage = ref();
        const modalIsOpen = ref(false);
        const currentSize = ref('');
        const acceptBuyModalOpen = ref(false);

        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);

        const setZoomImg = (image: string) => {
            activeImage.value = image;
            modalIsOpen.value = true;
        }

        const setCurrentSize = (size: string) => {
            currentSize.value = size;
        }

        const acceptBuy = () => {
            toast.showSuccess('merchBuySuccess');
            acceptBuyModalOpen.value = false
        }

        return {
            merchItemPlug,
            activeImage,
            modalIsOpen,
            currentSize,
            acceptBuyModalOpen,
            setZoomImg,
            setCurrentSize,
            acceptBuy,
        }
    }
})
</script>

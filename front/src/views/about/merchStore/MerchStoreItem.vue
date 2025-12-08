<template>
<div class="merch-store-item__wrapper">
    <div class="merch-store-item mt20">
        <div class="merch-store-item__images__wrapper">
            <div v-if="currentItem?.indirect_data && currentItem.indirect_data.images"
                 class="merch-store-item__images__flex-gallery">
                <div v-for="(card, index) in currentItem?.indirect_data?.images"
                     :key="index"
                     class="merch-store-item__images__flex-gallery__card__wrapper">
                    <div v-if="(typeof card !== 'string' && card.file_url)"
                         @click="setZoomImg(card.file_url)"
                         class="merch-store-item__images__flex-gallery__card">
                        <img class="pos-rel"
                             :src="(card.file_url)" />
                        <ZoomInIcon class="merch-store-item__images__flex-gallery__card__zoom-icon" />
                    </div>
                </div>
            </div>
            <HoverGallerySkeleton v-else />
        </div>
        <div class="merch-store-item__info"
             v-if="currentItem">
            <div class="merch-store-item__info__category"
                 v-if="currentItem.indirect_data?.category">{{ currentItem.indirect_data?.category }}</div>
            <h4 class="merch-store-item__info__title">
                {{ currentItem.name }}
            </h4>
            <div v-if="currentItem.content_text"
                 class="merch-store-item__info__description"
                 v-html="currentItem.content_text">
            </div>
            <div v-if="checkSizes(currentItem as IMerchItem).length !== 0 && currentSize !== 'no_size' && currentSize"
                 class="merch-store-item__info__sizes__title">
                <span>Размер</span>
                <div class="merch-store-item__info__sizes">
                    <div class="merch-store-item__info__size"
                         :class="{ 'merch-store-item__info__size--active': item == currentSize }"
                         v-for="item in checkSizes(currentItem as IMerchItem).filter((e) => e !== 'no_size')"
                         :key="'size' + item"
                         @click="setCurrentSize(item)">
                        {{ item }}
                    </div>
                </div>
            </div>

            <h3 class="merch-store-item__info__price">
                <span class="merch-store-item__info__count-text">
                    {{ currentItem?.indirect_data?.price }}
                </span>
                эмк-коинов
            </h3>

            <div v-if="currentSize && false"
                 class="merch-store-item__info__count">
                <span class="merch-store-item__info__count-text">
                    {{
                        currentItem?.indirect_data?.sizes_left[currentSize]
                    }}
                </span> шт. осталось
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
               :whiteBackground="true"
               :image="[activeImage]"
               @close="modalIsOpen = false" />

    <AcceptBuyModal v-if="acceptBuyModalOpen"
                    @closeModal="acceptBuyModalOpen = false"
                    @acceptBuy="(quantity: number) => acceptBuy(quantity)" />
</div>
</template>

<script lang="ts">
import ZoomModal from '@/components/tools/modal/ZoomModal.vue';
import { defineComponent, onMounted, ref } from 'vue';
import ZoomInIcon from "@/assets/icons/merchstore/ZoomInIcon.svg?component"
import AcceptBuyModal from './components/AcceptBuyModal.vue';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import Api from '@/utils/Api';
import type { IMerchItem } from '@/interfaces/entities/IMerch';
import { handleApiError, handleApiResponse } from '@/utils/apiResponseCheck';
import HoverGallerySkeleton from './components/HoverGallerySkeleton.vue';

export default defineComponent({
    components: {
        ZoomModal,
        ZoomInIcon,
        AcceptBuyModal,
        HoverGallerySkeleton
    },
    props: {
        id: {
            type: Number,
            default: 1
        },
    },
    setup(props) {
        const activeImage = ref();
        const modalIsOpen = ref(false);
        const currentSize = ref<'s' | 'm' | 'l' | 'xl' | 'xxl' | 'no_size'>('no_size');
        const acceptBuyModalOpen = ref(false);

        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);

        const currentItem = ref<IMerchItem>();

        const setZoomImg = (image: string) => {
            activeImage.value = image;
            modalIsOpen.value = true;
        }

        const setCurrentSize = (size: 's' | 'm' | 'l' | 'xl' | 'xxl' | 'no_size') => {
            currentSize.value = size;
        }

        const acceptBuy = async (quantity: number) => {
            if (!currentSize.value) return
            const sizeName = currentSize.value;
            toast.showWarning('merchBuyWarning');
            // await Api.put('store/create_purchase', { [sizeName]: quantity!, 'art_id': Number(currentItem.value?.id)! })
            //     .then((data) => {
            //         handleApiResponse(data, toast, 'trySupportError', 'merchBuySuccess')
            //     })
            //     .catch((error) => {
            //         handleApiError(error, toast)
            //     })
        }

        const checkSizes = (item: IMerchItem) =>
            Object.keys(item.indirect_data?.sizes_left ?? {}) as ('s' | 'm' | 'l' | 'xl' | 'xxl' | 'no_size')[];

        onMounted(() => {
            Api.get(`article/find_by_ID/${props.id}`)
                .then((data) => currentItem.value = data)
        })

        return {
            activeImage,
            modalIsOpen,
            currentSize,
            acceptBuyModalOpen,
            currentItem,
            setZoomImg,
            setCurrentSize,
            acceptBuy,
            checkSizes
        }
    }
})
</script>

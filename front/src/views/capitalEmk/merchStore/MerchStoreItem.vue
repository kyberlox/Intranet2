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
                             :class="{ 'merch-store-item__images__flex-gallery__card--cover': !card.file_url.includes('.png') }"
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
                 v-html="currentItem.content_text.replaceAll('&nbsp;', ' ')"></div>
            <div v-if="checkSizes(currentItem as IMerchItem).length !== 0"
                 class="merch-store-item__info__sizes__title">
                <!-- <span>Размер</span> -->
                <div class="merch-store-item__info__sizes">
                    <div class="merch-store-item__info__size"
                         :class="{ 'merch-store-item__info__size--active': item == currentSize }"
                         v-for="item in checkSizes(currentItem as IMerchItem).filter((e) => e !== 'no_size')"
                         :key="'size' + item"
                         @click="setCurrentSize(item as ('s' | 'm' | 'l' | 'xl' | 'xxl' | 'no_size'))">
                        {{ item }}
                    </div>
                </div>
            </div>

            <h3 v-if="currentItem?.indirect_data?.price"
                class="merch-store-item__info__price">
                <span class="merch-store-item__info__count-text">
                    {{ String(currentItem?.indirect_data?.price).replace(/(\d)(?=(\d{3})+([^\d]|$))/g, "$1 ") }}
                </span>
                баллов
            </h3>

            <div v-if="currentSize && false"
                 class="merch-store-item__info__count">
                <span class="merch-store-item__info__count-text">
                    {{
                        currentItem?.indirect_data?.sizes_left[currentSize as ("s" | "m" | "l" | "xl" | "xxl" | "no_size"
                        )]
                    }}
                </span> шт. осталось
            </div>
            <div class="merch-store-item__action__wrapper">
                <div @click="callModal(true)"
                     class="merch-store-item__action__button">
                    <span> Оформить</span>
                </div>
            </div>
        </div>
    </div>
    <ZoomModal v-if="modalIsOpen == true"
               :whiteBackground="true"
               :image="[activeImage]"
               @close="modalIsOpen = false" />

    <AcceptBuyModal v-if="acceptBuyModalOpen"
                    @closeModal="callModal(false)"
                    :price="currentItem?.indirect_data?.price"
                    :isLoading="isLoading"
                    :customPrice="currentItem?.indirect_data?.price ? false : true"
                    @acceptBuy="(quantity: number, customPrice: boolean) => acceptBuy(quantity, customPrice)" />
    <PurchaseSuccessModal v-if="purchaseSuccessModalOpen"
                          :itemName="currentItem?.name"
                          @close="purchaseSuccessModalOpen = false" />
</div>
</template>

<script lang="ts">
import ZoomModal from '@/components/tools/modal/ZoomModal.vue';
import { computed, defineComponent, onMounted, ref } from 'vue';
import ZoomInIcon from "@/assets/icons/merchstore/ZoomInIcon.svg?component"
import AcceptBuyModal from './components/AcceptBuyModal.vue';
import PurchaseSuccessModal from './components/PurchaseSuccessModal.vue';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import Api from '@/utils/Api';
import type { IMerchItem } from '@/interfaces/entities/IMerch';
import HoverGallerySkeleton from './components/HoverGallerySkeleton.vue';
import { featureFlags } from '@/assets/static/featureFlags';
import { useUserScore } from '@/stores/userScoreData';

const isResponseObject = (value: unknown): value is Record<string, unknown> => typeof value === 'object' && value !== null;

export default defineComponent({
    components: {
        ZoomModal,
        ZoomInIcon,
        AcceptBuyModal,
        PurchaseSuccessModal,
        HoverGallerySkeleton,
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
        const currentSize = ref<'s' | 'm' | 'l' | 'xl' | 'xxl' | 'no_size'>();
        const acceptBuyModalOpen = ref(false);
        const purchaseSuccessModalOpen = ref(false);
        const isLoading = ref(false);
        const currentScore = computed(() => useUserScore().getCurrentScore);

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

        const acceptBuy = async (quantity: number, customPrice: boolean = false) => {
            const routes = [
                {
                    route: 'store/create_purchase',
                    body: {
                        [currentSize.value as string]: quantity!,
                        'art_id': Number(currentItem.value?.id)!
                    }
                }, {
                    route: 'store/buy_split',
                    body: { 'art_id': Number(currentItem.value?.id)!, 'user_points': quantity }
                }]

            if (!featureFlags.pointsSystem) {
                toast.showWarning('merchBuyWarning');
            }
            else if ((customPrice && currentScore.value < quantity) || (!customPrice && currentItem.value?.indirect_data?.price && currentScore.value < currentItem.value?.indirect_data?.price)) {
                toast.showCustomToast('warn', 'К сожалению у вас недостаточно баллов')
            } else {
                const needRoute = quantity > 0 && !customPrice ? routes[0] : routes[1]
                try {
                    const data = await Api.put(needRoute.route, needRoute.body)
                    if (isResponseObject(data) && 'not_enough' in data) {
                        toast.showCustomToast('warn', 'К сожалению такого количества нет в наличии')
                    } else if (isResponseObject(data) && 'message' in data) {
                        toast.showCustomToast('warn', 'К сожалению у вас недостаточно баллов')
                    } else if (isResponseObject(data) && 'status' in data) {
                        toast.showCustomToast('warn', 'К сожалению у вас не хватает баллов')
                    } else if (!data) {
                        toast.showError('trySupportError');
                    }
                    else {
                        purchaseSuccessModalOpen.value = true;
                    }
                    try {
                        const points = await Api.get('/peer/user_history')
                        useUserScore().setStatistics(points)
                    } catch (error) {
                        console.error(error)
                    }
                } catch (error) {
                    console.error(error)
                } finally {
                    isLoading.value = false;
                    callModal(false);
                }
            }
        }

        const checkSizes = (item: IMerchItem) => {
            const sizes = Object.keys(item.indirect_data?.sizes_left ?? []);
            const notNullSizes: string[] = []
            sizes.forEach((e) => {
                if (item.indirect_data?.sizes_left[(e as keyof typeof item.indirect_data.sizes_left)] !== 0) {
                    notNullSizes.push(e)
                }
            })

            if (notNullSizes.length == 0 || (notNullSizes.length == 1 && notNullSizes[0] == 'no_size')) {
                currentSize.value = "no_size"
            }
            return notNullSizes
        }

        onMounted(async () => {
            try {
                const data = await Api.get(`article/find_by_ID/${props.id}`)
                currentItem.value = data
            } catch (error) {
                console.error(error)
            }
        })

        const callModal = (status: boolean) => {
            if (currentSize.value) {
                acceptBuyModalOpen.value = status;
            } else toast.showCustomToast('info', 'Выберите размер')
        }

        return {
            activeImage,
            modalIsOpen,
            currentSize,
            acceptBuyModalOpen,
            purchaseSuccessModalOpen,
            currentItem,
            isLoading,
            setZoomImg,
            setCurrentSize,
            acceptBuy,
            checkSizes,
            callModal
        }
    }
})
</script>

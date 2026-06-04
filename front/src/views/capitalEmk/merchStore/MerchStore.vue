<template>
<div class="mt20">
    <div class="merch-store__header">
        <div class="page__title">Магазин "Капитал ЭМК"</div>
        <button v-if="featureFlags.pointsSystem"
                class="primary-button merch-store__history-button"
                type="button"
                @click="purchaseHistoryOpen = true">
            История покупок
        </button>
    </div>
    <div class="merch-store__grid__wrapper">
        <div class="merch-store__grid"
             v-if="merchItems.length && !isLoading">
            <RouterLink :to="{ name: 'merchStoreItem', params: { id: item.id } }"
                        class="merch-store__grid__item"
                        v-for="item in sortedMerchItems"
                        :key="item.id">
                <div v-if="item.indirect_data?.images"
                     class="merch-store__grid__item__info">
                    <HoverGallery :coverFill="!item.indirect_data.price ? true : false"
                                  :showIndicators="true"
                                  :images="(item.indirect_data?.images as IBXFileType[])" />
                </div>
                <div class="merch-store__grid__item__title">
                    {{ item.name }}
                </div>
                <div v-if="item.indirect_data?.price"
                     class="merch-store__grid__item__price merch-store__grid__item__info__item__price merch-store__grid__item__info__item">
                    <span class="">
                        <strong>
                            {{
                                String(item.indirect_data?.price).replace(/(\d)(?=(\d{3})+([^\d]|$))/g, "$1 ")
                            }}
                        </strong>
                        баллов
                    </span>
                </div>
            </RouterLink>
        </div>
        <div class="merch-store__grid"
             v-else-if="isLoading">
            <HoverGallerySkeleton v-for="i in 8"
                                  :key="'merchplug' + i" />
        </div>
        <div v-else-if="!isLoading">
            <span>Тут пока пусто, следите за обновлениями</span>
        </div>
    </div>
    <SlotModal v-if="purchaseHistoryOpen && featureFlags.pointsSystem"
               @close="purchaseHistoryOpen = false">
        <div class="modal__text__content modal__text__content--user-points">
            <PointsInfoTable historyType="purchase" />
        </div>
    </SlotModal>
</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, computed, onUnmounted } from 'vue';
import HoverGallery from './components/HoverGallery.vue';
import Api from '@/utils/Api';
import { sectionTips } from '@/assets/static/sectionTips';
import type { IMerch } from '@/interfaces/entities/IMerch';
import type { IBXFileType } from '@/interfaces/IEntities';
import HoverGallerySkeleton from './components/HoverGallerySkeleton.vue';
import { usePointsData } from '@/stores/pointsData';
import { featureFlags } from '@/assets/static/featureFlags';
import SlotModal from '@/components/tools/modal/SlotModal.vue';
import PointsInfoTable from '@/views/user/userPointsComponents/PointsInfoTable.vue';

export default defineComponent({
    components: {
        HoverGallery,
        HoverGallerySkeleton,
        SlotModal,
        PointsInfoTable,
    },
    setup() {
        const abortController = new AbortController();
        const allActivities = computed(() => usePointsData().getActivities);
        const pointsAboutOpen = ref(false);
        const purchaseHistoryOpen = ref(false);
        const merchItems = ref<IMerch[]>([]);
        const isLoading = ref<boolean>(false);


        const sortedMerchItems = computed(() => {
            return [...merchItems.value].sort((a, b) => {
                const priceA = a.indirect_data?.price;
                const priceB = b.indirect_data?.price;

                // Если обе цены пустые, сохраняем порядок
                if (!priceA && !priceB) return 0;

                // Пустые цены в конец
                if (!priceA) return 1;
                if (!priceB) return -1;

                // Сортируем по числовому значению
                return Number(priceA) - Number(priceB);
            });
        });

        onMounted(async () => {
            isLoading.value = true;
            try {
                const data = await Api.get(`article/find_by/${sectionTips['МагазинМерча']}`, null, abortController.signal)
                merchItems.value = data
            } finally {
                isLoading.value = false
            }
        })

        onUnmounted(() => abortController.abort());

        return {
            merchItems,
            isLoading,
            allActivities,
            pointsAboutOpen,
            purchaseHistoryOpen,
            featureFlags,
            sortedMerchItems,
        }
    }
})
</script>

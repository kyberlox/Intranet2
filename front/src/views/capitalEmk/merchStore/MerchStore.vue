<template>
<div class="mt20">
    <div class="page__title"
         @click="console.log(merchItems)">Магазин "Капитал ЭМК"</div>
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
</div>
</template>

<script lang="ts">
import type { Swiper as SwiperType } from 'swiper';
import { Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import { defineComponent, onMounted, ref, computed } from 'vue';
import HoverGallery from './components/HoverGallery.vue';
import Api from '@/utils/Api';
import { sectionTips } from '@/assets/static/sectionTips';
import type { IMerch } from '@/interfaces/entities/IMerch';
import type { IBXFileType } from '@/interfaces/IEntities';
import HoverGallerySkeleton from './components/HoverGallerySkeleton.vue';
import { usePointsData } from '@/stores/pointsData';
import { featureFlags } from '@/assets/static/featureFlags';

export default defineComponent({
    components: {
        HoverGallery,
        HoverGallerySkeleton,
    },
    setup() {
        const allActivities = computed(() => usePointsData().getActivities);
        const pointsAboutOpen = ref(false);
        const merchItems = ref<IMerch[]>([]);
        const isLoading = ref<boolean>(false);
        const sliderConfig = {
            modules: [Pagination],
            slidesPerView: 1,
        };

        const swiperInstance = ref<SwiperType | null>(null);
        const swiperOn = (swiper: SwiperType) => {
            swiperInstance.value = swiper;
        }
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

        onMounted(() => {
            isLoading.value = true;
            Api.get(`article/find_by/${sectionTips['МагазинМерча']}`)
                .then((data) => merchItems.value = data)
                .finally(() => isLoading.value = false)
        })

        return {
            sliderConfig,
            merchItems,
            isLoading,
            allActivities,
            pointsAboutOpen,
            featureFlags,
            sortedMerchItems,
            swiperOn
        }
    }
})
</script>
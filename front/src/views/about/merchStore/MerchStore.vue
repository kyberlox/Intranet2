<template>
<div class="mt20">
    <div class="page__title">Магазин мерча</div>
    <div class="merch-store__grid__wrapper">
        <div class="merch-store__grid"
             v-if="merchItems.length">
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
        <div class="merch-store__grid"
             v-else>
            <HoverGallerySkeleton v-for="i in 8"
                                  :key="'merchplug' + i" />
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
import HoverGallerySkeleton from './components/HoverGallerySkeleton.vue';

export default defineComponent({
    components: {
        HoverGallery,
        HoverGallerySkeleton
    },
    setup() {
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
            sliderConfig,
            merchItems,
            swiperOn
        }
    }
})
</script>
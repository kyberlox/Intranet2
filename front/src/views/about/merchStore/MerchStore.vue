<template>
<div class="mt20">
    <div class="page__title">Капитал ЭМК</div>
    <div class="modal__text__content__points-info">
        <span>
            Уважаемые коллеги!
            <br />
            С 1 февраля стартует корпоративная программа «Капитал ЭМК»!
            <br />
            «Капитал ЭМК» — это ваш персональный бонусный клуб внутри компании: <br /> за труд, инициативу и достижения
            вы
            получаете баллы, которые можно обменять на товары из корпоративного каталога.
            <br />
        </span>
        <div class="modal__text__content__points-info__list"
             @click="pointsAboutOpen = !pointsAboutOpen">
            За что начисляют
        </div>
        <PointsAbout v-if="pointsAboutOpen"
                     :allActivities="allActivities" />
    </div>
    <div class="merch-store__grid__wrapper">
        <div class="merch-store__grid"
             v-if="merchItems.length && !isLoading">
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
import PointsAbout from '@/views/user/userPointsComponents/PointsAbout.vue';
import { usePointsData } from '@/stores/pointsData';
export default defineComponent({
    components: {
        HoverGallery,
        HoverGallerySkeleton,
        PointsAbout
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
            swiperOn
        }
    }
})
</script>
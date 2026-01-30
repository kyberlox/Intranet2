<template>
<div class="mt20">
    <div class="page__title">Капитал ЭМК</div>
    <div class="modal__text__content__points-info">
        <span>
            Уважаемые коллеги!
            <br />
            «Капитал ЭМК» — это ваш персональный бонусный клуб внутри компании: <br /> за труд, инициативу и достижения
            вы
            получаете баллы, которые можно обменять на товары из корпоративного каталога.
            <br />
            Ниже можно ознакомиться с перечнем активностей и стоимостью баллов за каждую из них.
        </span>
        <div class="block">
            <LayoutHeaderPointsModal :pointsAboutImportant="true" />
            <button class="primary-button">Магазин ЭМК</button>
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
import Api from '@/utils/Api';
import { sectionTips } from '@/assets/static/sectionTips';
import type { IMerch } from '@/interfaces/entities/IMerch';
import type { IBXFileType } from '@/interfaces/IEntities';
import { usePointsData } from '@/stores/pointsData';
import SlotModal from '@/components/tools/modal/SlotModal.vue';
import LayoutHeaderPointsModal from '@/components/layout/header/LayoutHeaderPointsModal.vue';
import { featureFlags } from '@/assets/static/featureFlags';

export default defineComponent({
    components: {
        LayoutHeaderPointsModal,
        SlotModal
    },
    setup() {
        const allActivities = computed(() => usePointsData().getActivities);
        const pointsAboutOpen = ref(false);
        const merchItems = ref<IMerch[]>([]);
        const isLoading = ref<boolean>(false);

        return {
            merchItems,
            isLoading,
            allActivities,
            pointsAboutOpen,
            featureFlags,
        }
    }
})
</script>

<style>
.block {
    display: flex;
    flex-direction: row;

}
</style>
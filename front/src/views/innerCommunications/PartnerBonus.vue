<template>
    <div class="page__title mt20">Предложения партнеров</div>
    <ComplexGallery class="mt20"
                    :page=page
                    :slides="bonusesSlides"
                    :routeTo="'partnerPost'" />
</template>
<script lang="ts">
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { computed, defineComponent, onMounted, type ComputedRef } from "vue";
import { sectionTips } from "@/assets/static/sectionTips";
import Api from "@/utils/Api";
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from "@/stores/loadingStore";
import type { IPartnerBonus } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        ComplexGallery
    },
    setup() {
        const bonusesSlides: ComputedRef<IPartnerBonus[]> = computed(() => useViewsDataStore().getData('partnerBonusData') as IPartnerBonus[]);
        onMounted(() => {
            if (bonusesSlides.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Бонусы партнеров']}`)
                .then((res) => useViewsDataStore().setData(res, "partnerBonusData"))
                .finally(() => {
                    useLoadingStore().setLoadingStatus(false);
                })
        })
        return {
            page: 'officialEvents',
            bonusesSlides
        };
    },
});
</script>
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
import type { IBaseEntity } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        ComplexGallery
    },
    setup() {
        const bonusesSlides: ComputedRef<IBaseEntity[]> = computed(() => useViewsDataStore().getData('partnerBonusData') as IBaseEntity[]);
        onMounted(() => {
            if (bonusesSlides.value.length) return;
            Api.get(`article/find_by/${sectionTips['БонусыПартнеров']}`)
                .then((res) => useViewsDataStore().setData(res, "partnerBonusData"))

        })
        return {
            page: 'officialEvents',
            bonusesSlides
        };
    },
});
</script>
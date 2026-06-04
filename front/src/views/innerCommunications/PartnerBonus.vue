<template>
<div class="page__title mt20">Предложения партнеров</div>
<ComplexGallery class="mt20"
                :page=page
                :slides="bonusesSlides"
                :routeTo="'partnerPost'" />
</template>
<script lang="ts">
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { computed, defineComponent, onMounted, onUnmounted, type ComputedRef } from "vue";
import { sectionTips } from "@/assets/static/sectionTips";
import Api from "@/utils/Api";
import { useViewsDataStore } from "@/stores/viewsData";
import type { IBaseEntity } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        ComplexGallery
    },
    setup() {
        const abortController = new AbortController();
        const bonusesSlides: ComputedRef<IBaseEntity[]> = computed(() => useViewsDataStore().getData('partnerBonusData') as IBaseEntity[]);
        onMounted(async () => {
            if (bonusesSlides.value.length) return;
            try {
                const res = await Api.get(`article/find_by/${sectionTips['БонусыПартнеров']}`, null, abortController.signal)
                useViewsDataStore().setData(res, "partnerBonusData")
            } catch (error) {
                console.error(error)
            }
        })

        onUnmounted(() => abortController.abort())

        return {
            page: 'officialEvents',
            bonusesSlides
        };
    },
});
</script>
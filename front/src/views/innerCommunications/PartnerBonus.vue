<template>
    <div class="page__title mt20">Предложения партнеров</div>
    <FlexGallery class="mt20"
                 :page=page
                 :slides="bonusesSlides"
                 :routeTo="'partnerPost'" />
</template>
<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { computed, defineComponent, onMounted, ref } from "vue";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import Api from "@/utils/Api";
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from "@/stores/loadingStore";
interface IFlexGallery {
    id: string
    title: string,
    img: string,
}

export default defineComponent({
    components: {
        FlexGallery
    },
    setup() {
        const bonusesSlides = computed(() => useViewsDataStore().getData('partnerBonusData'));
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
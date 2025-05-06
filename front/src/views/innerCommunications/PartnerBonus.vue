<template>
    <div class="page__title mt20">Предложения партнеров</div>
    <FlexGallery class="mt20"
                 :page=page
                 :slides="bonusesSlides"
                 :routeTo="'partnerPost'" />
</template>
<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { defineComponent, onMounted, ref } from "vue";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import Api from "@/utils/Api";
interface IFlexGallery {
    id: String
    title: String,
    img: String,
}

export default defineComponent({
    components: {
        FlexGallery
    },
    setup() {
        const bonusesSlides = ref();
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Бонусы партнеров']}`)
                .then((res) => bonusesSlides.value = res)
        })
        return {
            page: 'officialEvents',
            bonusesSlides
        };
    },
});
</script>
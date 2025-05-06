<template>
    <div class="page__title mt20">Афиша</div>
    <FlexGallery class="mt20"
                 :page=page
                 :slides="afisha" />
</template>
<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { defineComponent, onMounted, ref } from "vue";
import { slides } from '@/assets/staticJsons/corpEventsSlides';
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";

export default defineComponent({
    components: {
        FlexGallery
    },
    setup() {
        const afisha = ref();
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Афиша']}`)
                .then(res => afisha.value = res)
        })
        return {
            afisha,
            page: 'officialEvents'
        };
    },
});
</script>
<template>
    <div class="page__title mt20">Афиша</div>
    <FlexGallery class="mt20"
                 :page=page
                 :slides="afisha"
                 :routeTo="'eventAnnounce'" />
</template>
<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { defineComponent, onMounted, ref } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";

interface FlexGalleryElement {
    videoHref: String,
    img: String,
    title: String,
}

export default defineComponent({
    components: {
        FlexGallery
    },
    setup() {
        const afisha = ref();
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Афиша']}`)
                .then(res => afisha.value = res);
            console.log(afisha.value);

        })
        return {
            afisha,
            page: 'officialEvents'
        };
    },
});
</script>
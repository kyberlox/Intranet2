<template>
    <div class="page__title mt20">Афиша</div>
    <FlexGallery class="mt20"
                 :page=page
                 :slides="afisha"
                 :routeTo="'eventAnnounce'" />
</template>
<script lang="ts">
import FlexGallery from "@/components/tools/gallery/FlexGallery.vue";
import { computed, defineComponent, onMounted, ref } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from "@/stores/loadingStore";

interface FlexGalleryElement {
    videoHref: string,
    img: string,
    title: string,
}

export default defineComponent({
    components: {
        FlexGallery
    },
    setup() {
        const afisha = computed(() => useViewsDataStore().getData('afishaData'));
        onMounted(() => {
            if (afisha.value.length) return;
            useLoadingStore().setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Афиша']}`)
                .then(res => useViewsDataStore().setData(res, "afishaData"))
                .finally(() => {
                    useLoadingStore().setLoadingStatus(false);
                });

        })
        return {
            afisha,
            page: 'officialEvents'
        };
    },
});
</script>
<template>
    <div class="page__title mt20">Афиша</div>
    <ComplexGallery class="mt20"
                    :page=page
                    :slides="afisha"
                    :routeTo="'eventAnnounce'" />
</template>
<script lang="ts">
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { computed, defineComponent, onMounted, type ComputedRef } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from "@/stores/loadingStore";
import type { IAfishaItem } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        ComplexGallery
    },
    setup() {
        const afisha: ComputedRef<IAfishaItem[]> = computed(() => useViewsDataStore().getData('afishaData') as IAfishaItem[]);
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
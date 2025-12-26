<template>
<div class="page__title mt20">Афиша</div>
<ContentPlug v-if="!isLoading && !afisha.length"
             :needGptMark="true"
             :plugText="emptyPageHtml" />
<ComplexGallery v-else
                class="mt20"
                :page=page
                :slides="afisha"
                :routeTo="'eventAnnounce'" />
</template>
<script lang="ts">
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { computed, defineComponent, onMounted, type ComputedRef, ref } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import type { IAfishaItem } from "@/interfaces/IEntities";

import ContentPlug from '@/components/layout/ContentPlug.vue';
import { emptyPageHtml } from '@/assets/static/contentPlugs';

export default defineComponent({
    components: {
        ComplexGallery,
        ContentPlug
    },
    setup() {
        const afisha: ComputedRef<IAfishaItem[]> = computed(() => useViewsDataStore().getData('afishaData') as IAfishaItem[]);
        const isLoading = ref(true);
        onMounted(() => {
            if (afisha.value.length) return;
            Api.get(`article/find_by/${sectionTips['Афиша']}`)
                .then(res => useViewsDataStore().setData(res, "afishaData"))
                .finally(() => {
                    isLoading.value = false;
                });
        })

        return {
            afisha,
            isLoading,
            page: 'officialEvents',
            emptyPageHtml
        };
    },
});
</script>
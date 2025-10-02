<template>
<div class="page__title mt20">Афиша</div>
<PostSlug v-if="!isLoading && !afisha.length"
          :title="'Пока афиша пустая'"
          :text="'Но вы держитесь'" />
<ComplexGallery v-else
                class="mt20"
                :page=page
                :slides="afisha"
                :routeTo="'eventAnnounce'" />
</template>
<script lang="ts">
import ComplexGallery from "@/components/tools/gallery/complex/ComplexGallery.vue";
import { computed, defineComponent, onMounted, type ComputedRef, ref } from "vue";
import PostSlug from "@/components/tools/common/PostSlug.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import type { IAfishaItem } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        ComplexGallery,
        PostSlug
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
            page: 'officialEvents'
        };
    },
});
</script>
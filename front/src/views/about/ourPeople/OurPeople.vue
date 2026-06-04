<template>
<h2 class="page__title mt20">Наши люди</h2>
<GridGallery v-if="ourPeople"
             :gallery="ourPeople"
             :type="'ourPeople'"
             :routeTo="'ourPeopleInner'" />
</template>

<script lang="ts">
import { defineComponent, onMounted, computed, onUnmounted } from "vue";
import GridGallery from "@/components/tools/gallery/sample/SampleGallery.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import type { IOurPeople } from "@/interfaces/IEntities";

export default defineComponent({
    components: { GridGallery },
    setup() {
        const ViewsDataStore = useViewsDataStore();

        const ourPeople = computed((): IOurPeople[] => ViewsDataStore.getData('ourPeopleData') as IOurPeople[])
        const abortController = new AbortController();

        onMounted(async () => {
            if (ourPeople.value.length) return;
            try {
                const data = await Api.get(`article/find_by/${sectionTips['НашиЛюди']}`, null, abortController.signal)
                ViewsDataStore.setData(data, 'ourPeopleData');
            }
            catch (error) {
                console.error(error)
            }
        })

        onUnmounted(() => abortController.abort())

        return {
            ourPeople
        };
    },
});
</script>

<template>
    <h2 class="page__title mt20">Наши люди</h2>
    <GridGallery v-if="ourPeople"
                 :gallery="ourPeople"
                 :type="'ourPeople'" />
</template>

<script lang="ts">
import { defineComponent, onMounted, computed, watch } from "vue";
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";
import { useLoadingStore } from "@/stores/loadingStore"

export default defineComponent({
    components: { GridGallery },
    setup(props, { emit }) {
        const loadingStore = useLoadingStore();
        const ViewsDataStore = useViewsDataStore();
        const ourPeople = computed(() => ViewsDataStore.getData('ourPeopleData'));
        onMounted(() => {
            if (ourPeople.value.length) return;
            loadingStore.setLoadingStatus(true);
            Api.get(`article/find_by/${sectionTips['Наши люди']}`)
                .then((data) => {
                    ViewsDataStore.setData(data, 'ourPeopleData');
                });
        })
        watch(ourPeople, (newVal) => {
            if (newVal && newVal.length) {
                loadingStore.setLoadingStatus(false);
            }
        })
        return {
            ourPeople
        };
    },
});
</script>

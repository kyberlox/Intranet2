<template>
    <h2 class="page__title mt20">Наши люди</h2>
    <GridGallery v-if="ourPeople"
                 :gallery="ourPeople"
                 :type="'ourPeople'" />
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, computed, watch } from "vue";
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import { useViewsDataStore } from "@/stores/viewsData";


export default defineComponent({
    components: { GridGallery },
    setup(props, { emit }) {
        const ViewsDataStore = useViewsDataStore();
        const ourPeople = computed(()=>ViewsDataStore.getOurPeopleData);
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Наши люди']}`)
                .then((data) => {
                    ViewsDataStore.setOurPeopleData(data);
                });
        })
        watch(ourPeople, (newVal)=>{
            if(newVal && newVal.length){
                emit('hideLoader');
            }
        })
        return {
            ourPeople
        };
    },
});
</script>

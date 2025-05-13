<template>
    <div class="page__wrapper mt20">
        <h1 class="page__title">Видеорепортажи</h1>
        <GridGallery class="mt20"
                     :gallery="interviews"
                     :routeTo="'videoreport'"
                     :type="'video'" />
    </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import { onMounted, ref } from "vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";

export default defineComponent({
    components: { GridGallery },
    setup() {
        const interviews = ref([]);
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Видеорепортажи']}`)
                .then(res => {
                    interviews.value = res;
                })

        })
        return {
            interviews,
        };
    },
});
</script>

<template>
    <div class="page__wrapper mt20">
        <GridGallery :gallery="interviews"
                     :type="'video'" />
    </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import { interviews } from "@/assets/staticJsons/interviewExample";

export default defineComponent({
    components: { GridGallery },
    setup() {
        return {
            interviews,
        };
    },
});
</script>

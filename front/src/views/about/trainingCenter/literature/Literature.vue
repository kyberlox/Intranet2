<template>
    <div class="literature__training__page mt20">
        <div class="page__title">Учебные пособия и литература ЭМК</div>
        <TrainingTable :page="'literature'" />
    </div>
</template>

<script lang="ts">
import TrainingTable from "@/components/about/trainingCenter/TrainingTable.vue";
import { defineComponent } from "vue";
export default defineComponent({
    components: {
        TrainingTable,
    },
    setup() {
        return {};
    },
});
</script>

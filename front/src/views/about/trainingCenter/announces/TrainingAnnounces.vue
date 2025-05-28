<template>
    <div class="announces__training__page mt20">
        <div class="page__title">Проведённые тренинги</div>
        <TrainingTable :page="'announces'" />
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

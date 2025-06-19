<template>
    <div class="conducted-training__page mt20">
        <div class="page__title">Проведённые тренинги</div>
        <TrainingTable :page="'pastTrainings'" />
    </div>
</template>

<script lang="ts">
import TrainingTable from "../components/TrainingTable.vue";
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

<template>
<div class="announces__training__page mt20">
    <div class="page__title">
        Анонс учебных программ
    </div>
    <EmptyPagePlug />
    <!-- <TrainingTable :page="'announces'" /> -->
</div>
</template>

<script lang="ts">
// import TrainingTable from "../components/TrainingTable.vue";
import EmptyPagePlug from "@/components/layout/EmptyPagePlug.vue";
import { defineComponent } from "vue";
export default defineComponent({
    components: {
        EmptyPagePlug,
        // TrainingTable,
    },
    setup() {
        return {};
    },
});
</script>

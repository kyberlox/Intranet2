<template>
<div class="announces__training__page mt20">
    <div class="page__title">
        Анонс учебных программ
    </div>
    <ContentPlug :needGptMark="true"
                 :plugText="emptyPageHtml" />
    <!-- <TrainingTable :page="'announces'" /> -->
</div>
</template>

<script lang="ts">
// import TrainingTable from "../components/TrainingTable.vue";
import { emptyPageHtml } from '@/assets/static/contentPlugs';
import ContentPlug from '@/components/layout/ContentPlug.vue';

import { defineComponent } from "vue";
export default defineComponent({
    components: {
        ContentPlug,
        // TrainingTable,
    },
    setup() {
        return {
            emptyPageHtml
        };
    },
});
</script>

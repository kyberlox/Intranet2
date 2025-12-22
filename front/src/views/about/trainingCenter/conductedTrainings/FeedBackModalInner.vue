<template>
<div class="training-feedback__wrapper">
    <div class="training-feedback"
         v-for="(review, index) in trainingInModal?.indirect_data?.reviews"
         :key="index">
        <h1 v-if="review.reviewer"><span>{{ review.reviewer }}</span></h1>
        <h1 v-if="review.text"
            v-html="review.text"></h1>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import type { IConductedTrainings } from '@/interfaces/IEntities';

export default defineComponent({
    props: {
        trainingInModal: {
            type: Object as PropType<IConductedTrainings>
        }
    },
    setup() {
        return {
        }
    }
})
</script>
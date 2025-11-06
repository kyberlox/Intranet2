<template>
<div class="modal__text__content modal__text__content--user-points">
    <PointsInfoTable />
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import PointsInfoTable from '@/views/user/userPointsComponents/PointsInfoTable.vue';

export default defineComponent({
    components: {
        PointsInfoTable
    },
    setup() {
        return {

        }
    }
})
</script>
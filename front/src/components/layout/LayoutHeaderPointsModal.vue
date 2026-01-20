<template>
<div class="modal__text__content modal__text__content--user-points">
    <PointsInfoTable />
    <div class="modal__text__content__points-info">
        <span @click="pointsAboutOpen = !pointsAboutOpen">
            За что начисляют
        </span>
        <PointsAbout v-if="pointsAboutOpen"
                     :allActivities="allActivities" />
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import PointsInfoTable from '@/views/user/userPointsComponents/PointsInfoTable.vue';
import PointsAbout from '@/views/user/userPointsComponents/PointsAbout.vue';
import { usePointsData } from '@/stores/pointsData';

export default defineComponent({
    components: {
        PointsInfoTable,
        PointsAbout
    },
    setup() {
        const pointsAboutOpen = ref(false);
        const pointsData = usePointsData();
        const allActivities = computed(() => pointsData.getActivities);

        return {
            allActivities,
            pointsAboutOpen
        }
    }
})
</script>


<style scoped>
.modal__text__content__points-info {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    gap: 15px;

    &>span {
        color: var(--emk-brand-color) !important;
        cursor: pointer;
    }

    allActivities,

    &:hover {
        &>span {
            color: var(--emk-brand-color-dark) !important;
        }
    }
}
</style>
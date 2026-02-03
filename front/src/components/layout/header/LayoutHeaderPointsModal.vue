<template>
<div class="modal__text__content modal__text__content--user-points">
    <PointsInfoTable />
    <div class="modal__text__content__points-info__list">
        <a href="/about/capitalEmk/about"
           target="_blank"
           class="link">
            За что начисляют
        </a>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import PointsInfoTable from '@/views/user/userPointsComponents/PointsInfoTable.vue';
import { usePointsData } from '@/stores/pointsData';

export default defineComponent({
    components: {
        PointsInfoTable,
    },
    props: {
        pointsAboutImportant: {
            type: Boolean,
            default: () => false
        }
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
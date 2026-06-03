<template>
<div class="modal__text__content modal__text__content--user-points">
    <PointsInfoTable historyType="addition" />
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
import { defineComponent } from 'vue';
import PointsInfoTable from '@/views/user/userPointsComponents/PointsInfoTable.vue';

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
})
</script>

<template>
<tr class="activity-edit__row"
    v-for="active in activities"
    :key="active.id"
    data-row-id="14">
    <td class="activity-edit__cell activity-edit__cell--parameter">
        <div class="activity-edit__field">
            <PencilIcon />
            <input data-id="14"
                   data-type="activityName"
                   class="activity-edit__input activity-edit__input--name"
                   :value=active.name
                   aria-label="Название активности" />

        </div>
    </td>
    <td class="activity-edit__cell activity-edit__cell--cost">
        <div class="activity-edit__field">
            <PencilIcon />
            <input type="number"
                   max="999"
                   min="1"
                   class="activity-edit__input activity-edit__input--cost"
                   :value="active.coast"
                   aria-label="Стоимость балла" />
        </div>
    </td>
    <td class="activity-edit__cell activity-edit__cell--actions">
        <CancelIcon class="moderator__button cancelBtn"
                    @click="deleteItem(active.id)" />
    </td>
</tr>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import PencilIcon from '@/assets/icons/common/Pencil.svg?component';
import { usePointsData } from '@/stores/PointsData';
export default defineComponent({
    components: {
        CancelIcon,
        PencilIcon
    },
    emits: ['deleteItem'],
    setup(_, { emit }) {
        const activities = computed(() => usePointsData().getActivities);

        return {
            activities,
            deleteItem: (id: number) => emit('deleteItem', 'activity', id)
        }
    }
})
</script>

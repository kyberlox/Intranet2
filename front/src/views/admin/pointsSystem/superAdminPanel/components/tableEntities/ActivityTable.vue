<template>
<tr class="activity-edit__row"
    v-for="active in activities"
    :key="active.id"
    data-row-id="14">
    <td class="activity-edit__cell activity-edit__cell--parameter">
        <div class="activity-edit__field">
            <PencilIcon />
            <input data-type="activityName"
                   class="activity-edit__input activity-edit__input--name"
                   v-model="findActivity(active).name"
                   @change="$emit('editActivity', findActivity(active))" />
        </div>
    </td>
    <td class="activity-edit__cell activity-edit__cell--cost">
        <div class="activity-edit__field">
            <PencilIcon />
            <input type="number"
                   max="999"
                   min="1"
                   class="activity-edit__input activity-edit__input--cost"
                   v-model="findActivity(active).coast"
                   @change="$emit('editActivity', findActivity(active))" />
        </div>
    </td>
    <td class="activity-edit__cell activity-edit__cell--actions">
        <CancelIcon class="moderator__button cancelBtn"
                    @click="deleteItem(active.id)" />
    </td>
</tr>
</template>

<script lang="ts">
import { defineComponent, computed, ref } from 'vue';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import PencilIcon from '@/assets/icons/common/Pencil.svg?component';
import { usePointsData } from '@/stores/pointsData';
import type { INewActivityData } from '@/interfaces/IPutFetchData';

export default defineComponent({
    components: {
        CancelIcon,
        PencilIcon
    },
    emits: ['deleteItem', 'editActivity'],
    setup(_, { emit }) {
        const activities = computed(() => usePointsData().getActivities);
        const newActivities = ref<INewActivityData[]>(activities.value);

        const findActivity = (active: INewActivityData) => {
            const target = newActivities.value.findIndex((e) => e.id == active.id)
            if (target == -1) newActivities.value.push(active)
            return newActivities.value[newActivities.value.findIndex((e) => e.id == active.id)]
        }
        return {
            newActivities,
            activities,
            findActivity,
            deleteItem: (id: number) => emit('deleteItem', 'activity', id)
        }
    }
})
</script>

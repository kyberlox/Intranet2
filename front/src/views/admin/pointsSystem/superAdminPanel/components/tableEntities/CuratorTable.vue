<template>
<tr class="activity-edit__row"
    v-for="curator in curators"
    :key="curator.curator_id">
    <td class="activity-edit__cell activity-edit__cell--parameter">
        <div class="activity-edit__field">
            <span>
                {{ curator.curator_last_name + ' ' + curator.curator_name + ' ' + curator.curator_second_name }}
            </span>
        </div>
    </td>
    <td class="activity-edit__cell activity-edit__cell--cost">
        <div class="activity-edit__field">
            <span>
                {{ curator.activity_name }}
            </span>
        </div>
    </td>
    <td class="activity-edit__cell activity-edit__cell--actions">
        <CancelIcon class="moderator__button cancelBtn"
                    @click="$emit('deleteItem', 'curator', String(curator.curator_id), curator.activity_id)" />
    </td>
</tr>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import type { ICurator } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        CancelIcon,
    },
    props: {
        curators: {
            type: Array as PropType<ICurator[]>
        }
    },
    emits: ['deleteItem'],
})
</script>

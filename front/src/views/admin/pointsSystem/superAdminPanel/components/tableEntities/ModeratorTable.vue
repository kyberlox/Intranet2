<template>
<tr v-for="moder in moders"
    :key="moder.moder_id"
    class="activity-edit__row">
    <td class="activity-edit__cell activity-edit__cell--parameter">
        <div class="activity-edit__field">
            <span>
                {{ moder.moder_last_name + ' ' + moder.moder_name + ' ' + moder.moder_second_name }}
            </span>
        </div>
    </td>
    <td class="activity-edit__cell activity-edit__cell--actions">
        <CancelIcon class="moderator__button cancelBtn"
                    @click="$emit('deleteItem', 'moder', moder.moder_id)" />
    </td>
</tr>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import type { IPointsModer } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        CancelIcon,
    },
    props: {
        moders: {
            type: Array as PropType<IPointsModer[]>
        }
    },
    emits: ['deleteItem'],
})
</script>

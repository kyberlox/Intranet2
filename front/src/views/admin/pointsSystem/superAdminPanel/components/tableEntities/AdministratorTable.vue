<template>
<tr v-for="admin in admins"
    :key="admin.admin_id"
    class="activity-edit__row">
    <td class="activity-edit__cell activity-edit__cell--parameter">
        <div class="activity-edit__field">
            <span>
                {{ admin.admin_last_name + ' ' + admin.admin_name + ' ' + admin.admin_second_name }}
            </span>
        </div>
    </td>
    <td class="activity-edit__cell activity-edit__cell--actions">
        <CancelIcon class="moderator__button cancelBtn"
                    @click="$emit('deleteItem', 'admin', admin.admin_id)" />
    </td>
</tr>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import type { IPointsAdmin } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        CancelIcon,
    },
    props: {
        admins: {
            type: Array as PropType<IPointsAdmin[]>
        }
    },
    emits: ['deleteItem'],
})
</script>

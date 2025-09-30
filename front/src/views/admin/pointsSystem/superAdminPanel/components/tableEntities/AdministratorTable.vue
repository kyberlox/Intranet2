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
import { defineComponent, onMounted, ref } from 'vue';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import Api from '@/utils/Api';
import type { IPointsAdmin } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        CancelIcon,
    },
    emits: ['deleteItem'],
    setup() {
        const admins = ref<IPointsAdmin[]>([]);
        onMounted(() => {
            Api.get('peer/get_admins_list')
                .then((data) => { if (!data.status) admins.value = data })
        })
        return {
            admins
        }
    }
})
</script>

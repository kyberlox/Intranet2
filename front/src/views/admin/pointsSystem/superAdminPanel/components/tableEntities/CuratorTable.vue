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
                    @click="deleteItem(String(curator.curator_id))" />
    </td>
</tr>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import Api from '@/utils/Api';
import type { ICurator } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        CancelIcon,
    },
    emits: ['deleteItem'],
    setup(_, { emit }) {
        const curators = ref<ICurator[]>([])
        Api.get('peer/get_curators')
            .then((data: ICurator[]) => curators.value = data)
        return {
            curators,
            deleteItem: (id: string) => emit('deleteItem', id)
        }
    }
})
</script>

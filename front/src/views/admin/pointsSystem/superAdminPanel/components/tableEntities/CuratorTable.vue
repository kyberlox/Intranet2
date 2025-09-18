<template>
    <tr class="activity-edit__row"
        v-for="curator in curators"
        :key="curator.moder_id">
        <td class="activity-edit__cell activity-edit__cell--parameter">
            <div class="activity-edit__field">
                <span>
                    {{ curator.moder_id }}
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
            <CancelIcon class="moderator__button cancelBtn" />
        </td>
    </tr>

</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import Api from '@/utils/Api';

interface ICurator {
    activity_id: number,
    activity_name: string,
    moder_id: string
}

export default defineComponent({
    components: {
        CancelIcon,
    },
    setup() {
        const curators = ref<ICurator[]>([])
        Api.get('peer/get_moders')
            .then((data: ICurator[]) => curators.value = data)
        return {
            curators
        }
    }
})
</script>

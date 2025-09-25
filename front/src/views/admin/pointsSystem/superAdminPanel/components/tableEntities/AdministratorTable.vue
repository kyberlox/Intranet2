<template>
<tr class="activity-edit__row"
    data-row-id="14">
    <td class="activity-edit__cell activity-edit__cell--parameter">
        <div class="activity-edit__field">
            <span>
                Газинский Игорь Владимирович
            </span>
        </div>
    </td>
    <td class="activity-edit__cell activity-edit__cell--actions">
        <CancelIcon class="moderator__button cancelBtn" />
    </td>
</tr>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import Api from '@/utils/Api';

export default defineComponent({
    components: {
        CancelIcon,
    },
    setup() {
        onMounted(() => {
            Api.get('peer/get_admins_list')
                .then((data) => console.log(data))
        })
        return {

        }
    }
})
</script>

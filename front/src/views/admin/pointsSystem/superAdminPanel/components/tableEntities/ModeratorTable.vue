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
import { defineComponent } from 'vue';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
export default defineComponent({
    components: {
        CancelIcon,
    },
    setup() {
        return {

        }
    }
})
</script>

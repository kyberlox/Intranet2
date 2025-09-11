<template>
    <SlotModal @close="$emit('close')">
        <div class="send-points-form__wrapper">
            <AdminEditSelect :item="selectValue"
                             :yesOrNoFormat="false"
                             @pick="(value: string) => chosenActivity = value" />
            <span v-if="chosenActivity.value == 0">
                {{ usersActivities.likes_left }}
            </span>
            <AdminEditInput @pick="(value: string) => pointsComment = value"
                            :placeholder="'Укажите комментарий'" />
            <div class="send-points-formt__buttons">
                <div class="primary-button send-points-form__button send-points-form__button--cancel"
                     @click="$emit('close')">
                    <CancelIcon />
                </div>
                <div class="primary-button send-points-form__button send-points-form__button--accept"
                     :class="{ 'send-points-form__button--disabled': !pointsComment }"
                     @click="handlePointsSend">
                    <CheckIcon />
                </div>
            </div>
        </div>
    </SlotModal>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import AdminEditInput from '../components/inputFields/AdminEditInput.vue';
import CheckIcon from '@/assets/icons/common/Check.svg?component';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import SlotModal from '@/components/tools/modal/SlotModal.vue';
import AdminEditSelect from '../components/inputFields/AdminEditSelect.vue';
import { useUserScore } from '@/stores/userScoreData';
export default defineComponent({
    components: {
        AdminEditInput,
        CheckIcon,
        CancelIcon,
        SlotModal,
        AdminEditSelect
    },
    emits: ['close', 'sendPoints'],
    setup(props, { emit }) {
        const chosenActivity = ref();
        const pointsComment = ref<string>();
        const usersActivities = computed(() => useUserScore().getActions);
        const selectValue = { value: usersActivities.value.activities[0].value, values: usersActivities.value.activities }

        const handlePointsSend = () => {
            if (!pointsComment.value || !chosenActivity.value) return;
            emit('sendPoints', pointsComment.value, chosenActivity.value)
        }

        return {
            chosenActivity,
            pointsComment,
            selectValue,
            usersActivities,
            handlePointsSend
        }
    }
})
</script>
<style scoped lang="scss">
.send-points-form__wrapper {
    padding: 15px 20px 0 15px;
}

.send-points-formt__buttons {
    display: flex;
    flex-direction: row;
    gap: 5px;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.send-points-form__button {
    display: flex;

    &>svg {
        min-width: 30px;
        max-width: 30px;
    }

    &--cancel {
        &:hover {
            background: red;
        }
    }

    &--accept {
        &:hover:not(.disabled) {
            background: #4bad66;
        }
    }

    &--disabled {
        color: black !important;
        background: rgba(128, 128, 128, 0.41) !important;
    }
}
</style>
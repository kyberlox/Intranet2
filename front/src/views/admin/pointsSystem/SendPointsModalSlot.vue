<template>
<SlotModal @close="$emit('close')">
    <div class="send-points-form__wrapper">
        <AdminEditSelect :item="selectValue"
                         :yesOrNoFormat="false"
                         @pick="(value: string) => chosenActivity = value" />
        <AdminEditInput @pick="(value: string) => pointsComment = value"
                        :item="{ name: 'Укажите комментарий' }"
                        :placeholder="'...'" />
        <span class="send-points-form__warning"
              v-if="chosenActivity == 1">
            Осталось {{ usersActivities.likes_left }} отправлений по выбранной активности
        </span>
        <div class="send-points-form__buttons">
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
import { defineComponent, ref, computed, onMounted } from 'vue';
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
        const selectValue = ref();

        onMounted(() => {
            if (!usersActivities.value || !usersActivities.value.activities) return
            selectValue.value = { name: 'Выберите активность', value: usersActivities.value.activities[0].id ?? 0, values: usersActivities.value.activities }
        })

        const handlePointsSend = () => {
            console.log(pointsComment.value);
            console.log(chosenActivity.value);

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
<template>
<SlotModal @close="$emit('closeModal')">
    <div class="merch-store__accept-buy-modal__wrapper">
        <div class="merch-store__accept-buy-modal__content bug-modal__content">
            <p class="merch-store__accept-buy-modal__title">
                В форме ниже можете описать проблему с которой вы столкнулись или позвонить по номеру: 5182/5185
            </p>
            <textarea class="modal__input__text__input"
                      v-model="bugreport"></textarea>
        </div>
        <button @click="sendReport"
                class="primary-button">Подтвердить</button>
    </div>
</SlotModal>
</template>
<script lang='ts'>
import { defineComponent, ref, computed } from 'vue';
import SlotModal from '../tools/modal/SlotModal.vue';
import Api from '@/utils/Api';
import { createMail } from "@/utils/createMail";
import { useUserData } from '@/stores/userData';
import { handleApiError, handleApiResponse } from '@/utils/apiResponseCheck';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';

export default defineComponent({
    components: {
        SlotModal,
    },
    props: {},
    setup() {
        const bugreport = ref<string>('');
        const isLoading = ref(false);
        const email = computed(() => useUserData().getUser.email);
        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);

        const sendReport = () => {
            isLoading.value = true;
            if (!email.value || !bugreport.value) return;
            const mailText = createMail(bugreport.value, '');
            const body = {
                "sender": email.value,
                "reciever": '',
                "title": '',
                "text": mailText,
                "file_url": ''
            }
            Api.post('users/send_error', body)
                .then((data) => handleApiResponse(data, toast, 'trySupportError', 'sendPostCardSuccess'))
                .catch((e) => handleApiError(e, toast))
                .finally(() => isLoading.value = false)
        }

        return {
            bugreport,
            sendReport
        }
    }
});
</script>
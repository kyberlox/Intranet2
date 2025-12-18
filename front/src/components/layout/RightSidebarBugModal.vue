<template>
<SlotModal @close="$emit('closeModal')">
    <div class="merch-store__accept-buy-modal__wrapper">
        <div class="bug-modal__content">
            <p class="merch-store__accept-buy-modal__title">
                Заполните форму ниже или позвоните по телефону 5182/5185.
            </p>
            <textarea class="modal__input__text__input"
                      placeholder="Опишите проблему"
                      v-model="bugreport"></textarea>
        </div>
        <div>
            <button @click="sendReport"
                    class="primary-button">
                <Loader class="bug-modal__content__loader"
                        v-if="isLoading" />
                <span v-else>Подтвердить</span>

            </button>
        </div>

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
import Loader from './Loader.vue';

export default defineComponent({
    components: {
        SlotModal,
        Loader
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
            isLoading,
            sendReport
        }
    }
});
</script>
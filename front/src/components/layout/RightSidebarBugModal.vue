<template>
<SlotModal @close="$emit('closeModal')">
    <div class="merch-store__accept-buy-modal__wrapper">
        <div class="merch-store__accept-buy-modal__content">
            <p class="merch-store__accept-buy-modal__title">
                Опишите проблему с которой вы столкнулись, по скрепке можно
                приложить скриншот
            </p>

        </div>
        <button @click="sendReport"
                class="primary-button">Подтвердить</button>
    </div>
</SlotModal>
</template>
<script lang='ts'>
import { defineComponent } from 'vue';
import SlotModal from '../tools/modal/SlotModal.vue';

export default defineComponent({
    components: {
        SlotModal,
    },
    props: {},
    setup() {
        const sendReport = () => {
            console.log('Отправка')
        }
        return {
            sendReport
        }

    }
});
</script>
<style langs='scss'></style>
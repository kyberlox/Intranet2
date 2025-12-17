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
import { defineComponent, ref } from 'vue';
import SlotModal from '../tools/modal/SlotModal.vue';

export default defineComponent({
    components: {
        SlotModal,
    },
    props: {},
    setup() {
        const bugreport = ref<string>('');

        const sendReport = () => {
            console.log(bugreport)
        }
        return {
            bugreport,
            sendReport
        }
    }
});
</script>

<style lang="scss">
.bug-modal__content {
    display: flex;
    flex-direction: column;
}
</style>
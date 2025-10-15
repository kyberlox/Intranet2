<template>
<SlotModal @close="$emit('closeModal')">
    <div class="merch-store__accept-buy-modal__wrapper">
        <div class="merch-store__accept-buy-modal__content">
            <p class="merch-store__accept-buy-modal__title">Укажите кол-во:</p>

            <button class="merch-store__accept-buy-modal__quantity-input merch-store__accept-buy-modal__quantity-input--operation"
                    @click="quantity--">-</button>
            <input class="merch-store__accept-buy-modal__quantity-input"
                   type="number"
                   v-model="quantity"
                   min="0" />
            <button class="merch-store__accept-buy-modal__quantity-input merch-store__accept-buy-modal__quantity-input--operation"
                    @click="quantity++">+</button>

        </div>
        <button @click="accept"
                class="merch-store__accept-buy-modal__button">Подтвердить</button>
    </div>
</SlotModal>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import SlotModal from '@/components/tools/modal/SlotModal.vue';
export default defineComponent({
    components: {
        SlotModal
    },
    setup(props, { emit }) {
        const quantity = ref(1);
        watch((quantity), () => {
            if (quantity.value < 0) {
                quantity.value = 0
            }
        })

        return {
            quantity,
            accept: () => emit('acceptBuy', quantity.value)
        }
    }
})
</script>
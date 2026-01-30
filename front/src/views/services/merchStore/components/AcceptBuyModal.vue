<template>
<SlotModal @close="$emit('closeModal')">
    <div class="merch-store__accept-buy-modal__wrapper">
        <div class="merch-store__accept-buy-modal__content">
            <p class="merch-store__accept-buy-modal__title">
                {{
                    customPrice ? "Укажите, сколько баллов вы готовы потратить" : "Укажите кол - во"
                }}
            </p>
            <button v-if="!customPrice"
                    class="merch-store__accept-buy-modal__quantity-input merch-store__accept-buy-modal__quantity-input--operation"
                    @click="quantity--">-</button>
            <input class="merch-store__accept-buy-modal__quantity-input"
                   :class="{ 'merch-store__accept-buy-modal__quantity-input--custom-price': customPrice }"
                   type="number"
                   v-model="quantity"
                   min="0" />
            <button v-if="!customPrice"
                    class="merch-store__accept-buy-modal__quantity-input merch-store__accept-buy-modal__quantity-input--operation"
                    @click="quantity++">+</button>

        </div>
        <button @click="accept"
                class="merch-store__accept-buy-modal__button"
                :class="{ 'merch-store__accept-buy-modal__button--loading': isLoading }">
            <Loader v-if="isLoading" />
            <span v-else>Подтвердить</span>
        </button>
    </div>
</SlotModal>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import SlotModal from '@/components/tools/modal/SlotModal.vue';
import Loader from '@/components/layout/Loader.vue';

export default defineComponent({
    components: {
        SlotModal,
        Loader
    },
    props: {
        isLoading: {
            type: Boolean
        },
        customPrice: {
            type: Boolean,
            default: () => false
        }
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
            accept: () => emit('acceptBuy', quantity.value, props.customPrice)
        }
    }
})
</script>
<template>
<SlotModal @close="$emit('closeModal')">
    <div class="accept-buy-modal__wrapper">
        <div class="accept-buy-modal__content">
            <p class="accept-buy-modal__title">Укажите кол-во:</p>

            <button class="accept-buy-modal__quantity-input accept-buy-modal__quantity-input--operation"
                    @click="quantity--">-</button>
            <input class="accept-buy-modal__quantity-input"
                   type="number"
                   v-model="quantity"
                   min="0" />
            <button class="accept-buy-modal__quantity-input accept-buy-modal__quantity-input--operation"
                    @click="quantity++">+</button>

        </div>
        <button @click="accept"
                class="accept-buy-modal__button">Подтвердить</button>
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

<style lang="scss" scoped>
@use "@/assets/styles/mixins" as *;

.accept-buy-modal {
    &__wrapper {
        border-radius: 8px;
        padding: 2rem;
        width: 500px;
        margin: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        margin: auto;
        max-width: 100%;
    }

    &__quantity-input {
        width: 8ch;
        padding: 12px 0;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        font-size: 14px;
        line-height: 1.5;
        color: #303030;
        background: #ffffff;
        /* outline: none; */
        transition: all 0.2s ease;
        text-align: center;

        &--operation {
            width: 33px;
            padding: 6px 0;
            border-color: var(--emk-brand-color);

            &:hover {
                border-color: #ef7f1ba3;
            }
        }
    }

    &__content {
        display: flex;
        flex-direction: row;
        gap: 1rem;
        align-items: baseline;
        flex-wrap: nowrap;

        @include md {
            flex-direction: column;
            align-items: center;
        }
    }

    &__title {
        font-weight: 600;
        font-size: 16px;
        text-align: center;
    }



    &__button {
        width: 100%;
        padding: 12px;
        background: #ef7f1b;
        color: white;
        border: none;
        border-radius: 4px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.2s ease;

    }
}

// Адаптивность
@include md {
    .accept-buy-modal {
        &__wrapper {
            max-width: 350px;
            padding: 1.5rem;
        }
    }
}

@include sm {
    .accept-buy-modal {
        &__wrapper {
            max-width: 300px;
            padding: 1rem;

        }

        &__title {
            font-size: 14px;
        }

        &__button {
            padding: 10px;
            font-size: 13px;
        }
    }
}
</style>
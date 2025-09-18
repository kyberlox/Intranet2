<template>
<SlotModal>
    <div class="accept-buy-modal__wrapper">
        <div class="accept-buy-modal__content">
            <p class="accept-buy-modal__title">Укажите кол-во</p>
        </div>
        <button class="accept-buy-modal__button">Подтвердить</button>
    </div>
</SlotModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import SlotModal from '@/components/tools/modal/SlotModal.vue';
export default defineComponent({
    components: {
        SlotModal
    },
    setup() {
        return {

        }
    }
})
</script>

<style lang="scss" scoped>
@use "@/assets/styles/mixins/_mixins.scss" as *;

.accept-buy-modal {
    &__wrapper {
        background: white;
        border-radius: 8px;
        padding: 2rem;
        width: 100%;
        max-width: 400px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }

    &__content {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    &__title {
        font-style: normal;
        font-weight: 600;
        font-size: 16px;
        line-height: 20px;
        color: #303030;
        margin: 0;
        text-align: center;
    }

    &__input {
        width: 100%;

        :deep(.admin-edit-input) {
            width: 100%;

            input {
                width: 100%;
                padding: 12px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                font-size: 14px;
                outline: none;
                transition: border-color 0.2s ease;

                &:focus {
                    border-color: #ef7f1b;
                }
            }
        }
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

        &:hover {
            background: darken(#ef7f1b, 10%);
        }

        &:active {
            background: darken(#ef7f1b, 15%);
        }
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
            margin: 0 10px;
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
<template>
<SlotModal @close="$emit('close')">
    <div class="merch-store__success-modal__content">
        <div class="merch-store__success-modal__icon">
            <CheckIcon />
        </div>
        <div class="merch-store__success-modal__eyebrow">Магазин мерча</div>
        <h2 class="merch-store__success-modal__title">Заявка отправлена</h2>
        <p v-if="itemName"
           class="merch-store__success-modal__item">
            {{ itemName }}
        </p>
        <p class="merch-store__success-modal__text">
            Ваш запрос успешно отправлен. Скоро с вами свяжутся для уточнения деталей.
        </p>
        <button class="primary-button merch-store__success-modal__button"
                type="button"
                @click="$emit('close')">
            Вернуться в магазин
        </button>
    </div>
</SlotModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import CheckIcon from '@/assets/icons/common/Check.svg?component';
import SlotModal from '@/components/tools/modal/SlotModal.vue';

export default defineComponent({
    components: {
        CheckIcon,
        SlotModal,
    },
    props: {
        itemName: {
            type: String,
            default: ''
        }
    },
    emits: ['close']
})
</script>

<template>
    <div class="modal__overlay">
        <div class="modal__wrapper modal__wrapper--toast">
            <div class="modal__header modal__header--toast">
                <button class="modal__close-btn"
                        @click="closeToast"></button>
            </div>
            <div class="modal__body modal__body--review">
                <p>{{ toastText }}</p>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
    props: {
        toastText: String,
    },
    setup(props, { emit }) {
        return {
            closeToast: () => emit("closeToast"),
        };
    },
})
</script>

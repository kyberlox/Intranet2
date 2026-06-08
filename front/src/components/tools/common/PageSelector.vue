<template>
<div class="page-selector">
    <button type="button"
            :class="[buttonClass, 'page-selector__button primary-button']"
            :disabled="isLoading"
            @click="emitPageChange">
        Посмотреть еще
    </button>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    props: {
        isLoading: {
            type: Boolean,
            default: false
        },
        buttonClass: {
            type: String,
            default: 'btn'
        }
    },
    emits: ['loadMore'],
    setup(_, { emit }) {

        const emitPageChange = () => {
            emit('loadMore');
        }

        return {
            emitPageChange,
        };
    },
});
</script>

<style scoped>
.page-selector {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin: 28px 0 8px;
}



.page-selector__field {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
}
</style>

<template>
<div class="page-selector">
    <button class='primary-button'
            :class="{ 'page-selector__button--disabled': isLimit }"
            :disabled="isLoading"
            @click="emitPageChange">
        <span v-if="!isLimit || isLoading">Посмотреть еще</span>
        <span v-else>Вы посмотрели все статьи</span>
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
        },
        isLimit: {
            type: Boolean,
            default: false
        }
    },
    emits: ['loadMore'],
    setup(props, { emit }) {

        const emitPageChange = () => {
            if (!props.isLimit)
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

.page-selector__button--disabled {
    background: rgb(193 193 193 / 39%) !important;
    border: 1px solid #bdbdbd;

    &:hover {
        background: rgb(193 193 193 / 39%) !important;
        border: 1px solid #bdbdbd;
        color: black;
        cursor: not-allowed;
    }
}
</style>

<template>
<div class="page-selector">
    <button type="button"
            :class="[buttonClass, 'page-selector__button']"
            :disabled="page === 0 || isLoading"
            @click="emitPageChange(page)">
        Назад
    </button>
    <label class="page-selector__field">
        <span>Страница</span>
        <input class="page-selector__input"
               type="number"
               min="1"
               :value="page + 1"
               :disabled="isLoading"
               @change="handleInputChange" />
    </label>
    <button type="button"
            :class="[buttonClass, 'page-selector__button']"
            :disabled="isLoading"
            @click="emitPageChange(page + 2)">
        Вперед
    </button>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    props: {
        page: {
            type: Number,
            required: true
        },
        isLoading: {
            type: Boolean,
            default: false
        },
        buttonClass: {
            type: String,
            default: 'btn'
        }
    },
    emits: ['changePage'],
    setup(_, { emit }) {
        const emitPageChange = (newPage: number) => {
            emit('changePage', newPage);
        }

        const handleInputChange = (event: Event) => {
            emitPageChange(Number((event.target as HTMLInputElement).value));
        }

        return {
            emitPageChange,
            handleInputChange
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

.page-selector__button {
    min-width: 92px;
    border: 1px solid #d7d7d7;
}

.page-selector__field {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
}

.page-selector__input {
    width: 72px;
    height: 38px;
    padding: 6px 10px;
    border: 1px solid #d7d7d7;
    border-radius: 4px;
}
</style>

<template>
    <div class="loader">
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    setup() {
        return {

        }
    }
})
</script>

<style>
.loader {
    width: 64px;
    height: 64px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid var(--emk-brand-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>
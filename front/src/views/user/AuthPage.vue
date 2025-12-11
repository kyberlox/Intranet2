<template>
<div class="portal__auth">
    <div class="portal__auth__bg"></div>
    <div class="portal__auth__content">
        <div class="portal__auth__message"> </div>
        <div class="portal__auth__form__auth">
            <button class="btn btn-primary portal__auth__form__auth__submit"
                    @click="tryLogin">
                <span v-if="!isLoading"> Войти</span>
                <Loader v-else-if="isLoading"
                        class="pos-rel" />
            </button>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Loader from '@/components/layout/Loader.vue';
import { useRouter } from 'vue-router';

export default defineComponent({
    name: 'AuthPage',
    components: {
        Loader
    },
    setup() {
        const router = useRouter();
        const isLoading = ref(false);
        const tryLogin = () => {
            isLoading.value = true
            router.push({ name: 'oauthPage' })
        }

        return {
            isLoading,
            tryLogin
        };
    },
})
</script>
<template>
<div class="portal__auth"
     @keyup.enter="tryLogin"
     tabindex="0">
    <div class="portal__auth__bg"></div>
    <div class="portal__auth__content">
        <div class="portal__auth__form__auth">
            <button @click="tryLogin"
                    class="btn btn-primary portal__auth__form__auth__submit">
                <span v-if="!isLoading">Войти</span>
                <Loader v-else
                        class="pos-rel" />
            </button>
        </div>
        <input v-if="testMode"
               v-model="login" />
        <input v-if="testMode"
               v-model="pass" />
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import Loader from '@/components/layout/Loader.vue';
import { useRoute, useRouter } from 'vue-router';
import { testMode } from '@/assets/static/testMode';
import Api from '@/utils/Api';
import { useUserData } from '@/stores/userData';

export default defineComponent({
    name: 'AuthPage',
    components: {
        Loader
    },
    setup() {
        const router = useRouter();
        const route = useRoute();
        const isLoading = ref(false);
        const login = ref();
        const pass = ref();

        const tryLogin = () => {
            isLoading.value = true
            if (testMode) {
                testLogin()
            }
            else {
                router.push({ name: 'oauthPage', params: { referrer: import.meta.env.VITE_API_URL.replace('/api', '') + route.fullPath } })
            }
            isLoading.value = false
        }

        const testLogin = () => {
            Api.post("auth_router/root_auth", { login: login.value, password: pass.value })
                .then((data) => {
                    useUserData().setAuthKey(data.session_id)
                    useUserData().setLogin(true)
                    useUserData().setMyId(2366)
                })
        }

        watch((route), () => {
            if (!useUserData().getIsLogin) {
                localStorage.setItem('from', String(route.name));
            }
        }, { immediate: true, deep: true })


        return {
            login,
            pass,
            isLoading,
            testMode,
            tryLogin
        };
    },
})
</script>
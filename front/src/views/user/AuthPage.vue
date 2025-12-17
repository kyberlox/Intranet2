<template>
<div class="portal__auth">
    <div class="portal__auth__bg"></div>
    <div class="portal__auth__content">
        <div class="portal__auth__message"> </div>
        <div class="portal__auth__form__auth">
            <button class="btn btn-primary portal__auth__form__auth__submit"
                    @keyup.enter="tryLogin"
                    @click="tryLogin">
                <span v-if="!isLoading"> Войти</span>
                <Loader v-else-if="isLoading"
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
import { defineComponent, ref } from 'vue';
import Loader from '@/components/layout/Loader.vue';
import { useRouter } from 'vue-router';
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
        const isLoading = ref(false);
        const login = ref();
        const pass = ref();

        const tryLogin = () => {
            isLoading.value = true
            if (testMode) {
                testLogin()
            }
            else {
                router.push({ name: 'oauthPage' })
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
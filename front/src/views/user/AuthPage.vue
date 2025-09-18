<template>
<div class="portal__auth">
    <div class="portal__auth__bg"></div>
    <div class="portal__auth__content">
        <div class="portal__auth__message"> </div>
        <div class="portal__auth__form__auth">
            <div class="portal__auth__form__input__block">
                <input class="bx-auth-input form-control portal__auth__form__input"
                       placeholder="Логин"
                       name="authLogin"
                       type="text"
                       autocomplete="on"
                       @keydown="handleKeyDown"
                       ref="loginInput"
                       v-model="userName">
            </div>
            <div class="portal__auth__form__input__block">
                <input class="bx-auth-input form-control portal__auth__form__input"
                       type="password"
                       name="authPass"
                       autocomplete="on"
                       placeholder="Пароль"
                       @keydown="handleKeyDown"
                       v-model="passWord">
            </div>
            <button class="btn btn-primary portal__auth__form__auth__submit"
                    name="Login"
                    @click="tryLogin">
                Войти
            </button>
            <div class="portal__auth__form__error">{{ error ? error : '' }}</div>
        </div>
    </div>
</div>
</template>
<script lang="ts">
import { useUserData } from '@/stores/userData';
import Api from '@/utils/Api';
import { defineComponent, onMounted, ref } from 'vue';
import { handleApiError } from '@/utils/ApiResponseCheck';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import { prefetchSection } from '@/composables/usePrefetchSection';

export default defineComponent({
    name: 'AuthPage',
    components: {},
    setup() {
        const userName = ref('');
        const passWord = ref('');
        const error = ref();
        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);
        const loginInput = ref();
        const tryLogin = () => {
            if (!userName.value || !passWord.value) {
                return error.value = 'Проверьте логин и пароль'
            }
            else
                Api.post('auth_router/auth', { login: userName.value, password: passWord.value })
                    .then((resp) => {
                        if (resp.session_id) {
                            localStorage.setItem('authKey', resp.session_id);
                            useUserData().setAuthKey(resp.session_id);
                            useUserData().setMyId(resp.user.ID)
                            if (useUserData().getMyId !== 0) {
                                useUserData().setLogin(true);
                                prefetchSection('user');
                            }
                        }
                        else if (resp.warn) {
                            if (String(resp.warn).includes('login') || String(resp.warn).includes('password')) {
                                error.value = 'Ошибка авторизации. Проверьте логин и пароль'
                            }
                            else error.value = 'Что-то пошло не так. Повторите попытку или сообщите в поддержку сайта (5182/5185)'
                        }
                    })
                    .catch((error) => {
                        handleApiError(error, toast)
                    })
        }

        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                tryLogin();
            }
        }

        onMounted(() => {
            loginInput.value.focus();
        })

        return {
            userName,
            passWord,
            error,
            loginInput,
            tryLogin,
            handleKeyDown
        };
    },
})
</script>
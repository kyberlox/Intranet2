<template>
    <div class="portal__auth">
        <div class="portal__auth__bg"></div>
        <div class="portal__auth__content">
            <div class="portal__auth__message"> </div>
            <div class="portal__auth__form__auth">
                <div class="portal__auth__form__input__block">
                    <input class="bx-auth-input form-control portal__auth__form__input"
                           placeholder="Логин"
                           v-model="userName">
                </div>
                <div class="portal__auth__form__input__block">
                    <input class="bx-auth-input form-control portal__auth__form__input"
                           type="password"
                           autocomplete="off"
                           placeholder="Пароль"
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
import { defineComponent, ref } from 'vue';

export default defineComponent({
    name: 'AuthPage',
    components: {},
    setup() {
        const userName = ref('');
        const passWord = ref('');
        const error = ref();

        const tryLogin = async () => {
            await Api.post('auth_router/auth', { login: "abobus", password: "1" })
                .then((resp) => {
                    if (resp.session_id) {

                        localStorage.setItem('authKey', resp.session_id);
                        useUserData().setAuthKey(resp.session_id);
                        useUserData().setLogin(true);
                    }
                    else if (resp.warn) {
                        if (String(resp.warn).includes('login') || String(resp.warn).includes('password')) {
                            error.value = 'Ошибка авторизации. Проверьте логин и пароль'
                        }
                        else error.value = 'Что-то пошло не так. Повторите попытку или сообщите в поддержку сайта (5182/5185)'
                    }
                })
        }
        return {
            tryLogin,
            userName,
            passWord,
            error
        };
    },
})
</script>
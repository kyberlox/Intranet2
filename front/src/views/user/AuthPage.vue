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
                     </div>
              </div>
       </div>
</template>
<script lang="ts">
import { useUserData } from '@/stores/userData';
import Api from '@/utils/Api';
import { defineComponent, onMounted, ref } from 'vue';

export default defineComponent({
       name: 'AuthPage',
       components: {},
       setup() {
              const userName = ref('');
              const passWord = ref('');

              const tryLogin = async () => {
                     await Api.post('auth_router/auth', { login: "abobus", password: "1" })
                            .then((resp) => {
                                   if (resp.session_id) {
                                          localStorage.setItem('authKey', resp.session_id);
                                          useUserData().setAuthKey(resp.session_id);
                                          useUserData().setLogin(true);
                                   }
                            })
              }
              return {
                     tryLogin,
                     userName,
                     passWord
              };
       },
})
</script>
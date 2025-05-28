<template>
       <div class="portal__auth">
              <div class="portal__auth__bg"></div>
              <div class="portal__auth__content">
                     <div class="portal__auth__message"> </div>
                     <form name="form_auth"
                           method="post"
                           target="_top"
                           action="/intranet/?login=yes"
                           class="portal__auth__form__auth">
                            <input type="hidden"
                                   name="AUTH_FORM"
                                   value="Y">
                            <input type="hidden"
                                   name="TYPE"
                                   value="AUTH">
                            <input type="hidden"
                                   name="backurl"
                                   value="/intranet/">
                            <div class="portal__auth__form__input__block">
                                   <input class="bx-auth-input form-control portal__auth__form__input"
                                          type="text"
                                          name="USER_LOGIN"
                                          maxlength="255"
                                          value="gazinskii.i.v"
                                          placeholder="Логин">
                            </div>
                            <div class="portal__auth__form__input__block">
                                   <input class="bx-auth-input form-control portal__auth__form__input"
                                          type="password"
                                          name="USER_PASSWORD"
                                          maxlength="255"
                                          autocomplete="off"
                                          placeholder="Пароль">
                            </div>

                            <div class="portal__auth__form__remember">
                                   <input type="checkbox"
                                          id="USER_REMEMBER"
                                          name="USER_REMEMBER"
                                          value="Y"><label for="USER_REMEMBER">&nbsp;<span>Запомнить меня на этом
                                                 компьютере</span></label>
                            </div>

                            <input type="submit"
                                   class="btn btn-primary portal__auth__form__auth__submit"
                                   name="Login"
                                   value="Войти">
                     </form>
              </div>
       </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
       name: 'AuthPage',
       components: {},
       setup() {
              return {};
       },
})
</script>
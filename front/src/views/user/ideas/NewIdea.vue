<template>
<div class="mt20">
    <h2 class="page__title">Обратная связь: Есть идея!</h2>
    <div class="page__description"
         v-html="greetings"></div>
    <div class="col-sm-6 mt20">
        <VForm class="form-floating idea-new__form-floating idea-new__form mb-3"
               ref="formRef"
               @submit="sendIdea">

            <!-- Поле темы -->
            <div class="idea-new__form__invalid-feedback__wrapper">
                <ErrorMessage name="themeField"
                              class="idea-new__form__invalid-feedback" />
            </div>
            <div class="form-floating idea-new__form-floating">
                <Field class="form-control"
                       name="themeField"
                       :rules="isRequired"
                       type="text"
                       v-model="messageTheme"
                       placeholder="Тема" />
                <label for="themeField">Тема</label>
            </div>

            <!-- Поле сообщения -->
            <div class="idea-new__form__invalid-feedback__wrapper">
                <ErrorMessage name="textField"
                              class="idea-new__form__invalid-feedback" />
            </div>
            <div class="form-floating idea-new__form-floating">
                <Field as="textarea"
                       class="form-control idea-new__textarea"
                       name="textField"
                       :rules="isRequired"
                       rows="8"
                       placeholder="Добавьте сообщение"
                       v-model="messageText" />
                <label for="textField">Сообщение</label>
            </div>

            <!-- Поле файла -->
            <div class="">
                <label for="formFile"
                       class="form-label">Добавить файл</label>
                <input class="form-control"
                       name="attachments-files"
                       ref="fileInput"
                       type="file"
                       @change="handleMessageFileLoad">
            </div>

            <!-- Кнопка отправки -->
            <div class="mb-3 mt20">
                <button :class="{ 'primary-button--disabled': buttonsIsDisabled }"
                        :disabled="buttonsIsDisabled"
                        class="primary-button">
                    Отправить
                </button>
            </div>
        </VForm>
    </div>
</div>
</template>

<script lang="ts">
import Api from '@/utils/Api';
import { ref, type Ref, defineComponent } from 'vue';
import { useBase64 } from '@vueuse/core'
import { shallowRef } from 'vue'
import { type IPostIdea } from '@/interfaces/IPostFetch';
import { Field, Form as VForm, ErrorMessage, type GenericObject } from 'vee-validate';

export default defineComponent({
    name: 'NewIdea',
    components: {
        Field,
        VForm,
        ErrorMessage
    },
    emits: ['showToast'],
    setup(props, { emit }) {
        const messageText: Ref<string> = ref('');
        const messageTheme: Ref<string> = ref('');
        const messageFile = shallowRef<File>();
        const messageFileName = ref("");
        const fileInput = ref();
        const formRef = ref();

        const { base64: fileBase64 } = useBase64(messageFile);

        const handleMessageFileLoad = (e: Event) => {
            const target = e.target as HTMLInputElement;
            if (target.files && target.files[0]) {
                messageFileName.value = target.files[0].name;
                messageFile.value = target.files[0];
            }
        };

        const buttonsIsDisabled = ref(false);

        const sendIdea = (values: GenericObject) => {
            buttonsIsDisabled.value = true;

            const formData: IPostIdea = {};
            formData.NAME = values.themeField;
            formData.DETAIL_TEXT = values.textField;
            formData.CREATED_BY = '2366';
            formData.base_name = messageFileName.value;

            if (fileBase64.value) {
                formData.base = fileBase64.value.split(',')[1];
            }

            Api.post('/idea/new/', formData)
                .then((data) => {
                    if (!data || Boolean(data.data) == false) {
                        emit('showToast', 'error', 'Что-то пошло не так, попробуйте обновить страницу и повторить или сообщите в поддержку сайта (5182/5185)');
                    }
                    else {
                        clearForm();
                        emit('showToast', 'success', 'Идея успешно отправлена! Спасибо!');
                    }
                })
                .catch((error) => {
                    if (error.response?.status === 401) {
                        emit('showToast', 'error', 'Необходимо заново авторизоваться, пожалуйста, обновите страницу и попробуйте еще раз');
                    }
                    else
                        emit('showToast', 'error', 'Ошибка сервера, пожалуйста, сообщите в поддержку сайта (5182/5185)');
                })
                .finally(() => buttonsIsDisabled.value = false)
        };

        const clearForm = () => {
            if (formRef.value) {
                formRef.value.resetForm();
            }
        };

        const isRequired = (inputValue: unknown) => {
            if (inputValue && String(inputValue).trim()) {
                return true;
            }
            return 'Пропущены обязательные поля';
        };

        return {
            messageText,
            messageTheme,
            fileBase64,
            fileInput,
            buttonsIsDisabled,
            formRef,
            handleMessageFileLoad,
            sendIdea,
            isRequired,
            greetings: `<p>Добро пожаловать на страницу обратной связи нашего внутрикорпоративного сайта
            Интранет!</p>
        <p>Здесь вы можете поделиться своими идеями и предложениями по улучшению работы компании.</p>
        <p>Ваши идеи могут быть связаны с улучшением бизнес-процессов в компании, с производством, качеством, созданием
            новой техники, повышением квалификации, оптимизации работы в отдельном подразделении или
            внутрикорпоративными событиями.</p>
        <p>Мы всегда открыты к новым идеям и готовы выслушать каждого сотрудника.
            Давайте работать вместе и делать нашу
            компанию еще лучше!</p>`
        }
    }
})
</script>
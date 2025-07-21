<template>
    <div class="mt20">
        <h2 class="page__title">Обратная связь: Есть идея!</h2>
        <div class="page__description"
             v-html="greetings"></div>
        <div class="col-sm-6">
            <Form class="form-floating new-idea__form mb-3"
                  ref="formRef"
                  @submit="sendIdea">

                <!-- Поле темы -->
                <div class="invalid-feedback__wrapper">
                    <ErrorMessage name="themeField"
                                  class="invalid-feedback" />
                </div>
                <div class="form-floating">
                    <Field class="form-control"
                           name="themeField"
                           :rules="isRequired"
                           type="text"
                           v-model="messageTheme"
                           placeholder="Тема" />
                    <label for="themeField">Тема</label>
                </div>

                <!-- Поле сообщения -->
                <div class="invalid-feedback__wrapper">
                    <ErrorMessage name="textField"
                                  class="invalid-feedback" />
                </div>
                <div class="form-floating">
                    <Field as="textarea"
                           class="form-control new-idea__textarea"
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
                <div class="mb-3">
                    <button :class="{ 'primary-button--disabled': buttonsIsDisabled }"
                            :disabled="buttonsIsDisabled"
                            class="primary-button">
                        Отправить
                    </button>
                </div>
            </Form>
        </div>
        <Toast position="bottom-right" />
    </div>
</template>

<script lang="ts">
import Api from '@/utils/Api';
import { ref, type Ref, defineComponent } from 'vue';
import { useBase64 } from '@vueuse/core'
import { shallowRef } from 'vue'
import { type IPostIdea } from '@/interfaces/IPostFetch';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import { Field, Form, ErrorMessage, type GenericObject } from 'vee-validate';

export default defineComponent({
    name: 'NewIdea',
    components: {
        Toast,
        Field,
        Form,
        ErrorMessage
    },
    setup() {
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
        const toast = useToast();

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
                    if (!data) {
                        show('error', 'Что-то пошло не так, попробуйте повторить позже');
                    } else {
                        clearForm();
                        show('success', 'Идея успешно отправлена, спасибо!');
                    }
                })
                .finally(() => buttonsIsDisabled.value = false)
        };

        const show = (type: string, text: string) => {
            toast.add({ severity: type, summary: type, detail: text, life: 13000 });
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
            show,
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

<style lang="scss">
.new-idea__form {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.invalid-feedback {
    display: block;
    width: 100%;
    font-size: 0.875em;
    color: #dc3545;
    min-height: 21px;

    &__wrapper {
        min-height: 21px;
    }
}

.new-idea__textarea {
    height: auto !important;
}

.primary-button--disabled {
    background: #d1d0d09a;
    cursor: not-allowed;

    &:hover {
        color: black;
        background: #d1d0d09a;
    }
}

.form-floating>.form-control:focus {
    padding: 1rem 0.75rem !important;
}

/* Остальные стили Toast */
.p-toast {
    z-index: 9999;
}

.p-toast-message {
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    padding: 10px;
    gap: 5px;
}

.p-toast-message-success {
    background: #16a34aad !important;
    border: 1px solid #c3e6cb !important;
    color: black !important;
}

.p-toast-message-error {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
}

.p-toast-summary {
    display: none;
}

.p-toast-detail {
    margin: 0;
    line-height: 1.4;
}

.p-icon {
    margin: auto !important;
}

.form-floating>label {
    opacity: 0.6;
}
</style>

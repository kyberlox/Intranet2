<template>
    <div class="mt20">
        <h2 class="page__title">Обратная связь: Есть идея!</h2>
        <p>Добро пожаловать на страницу обратной связи нашего внутрикорпоративного сайта
            Интранет!</p>
        <p>Здесь вы можете поделиться своими идеями и предложениями по улучшению работы компании.</p>
        <p>Ваши идеи могут быть связаны с улучшением бизнес-процессов в компании, с производством, качеством, созданием
            новой техники, повышением квалификации, оптимизации работы в отдельном подразделении или
            внутрикорпоративными событиями.</p>
        <p>Мы всегда открыты к новым идеям и готовы выслушать каждого сотрудника. Давайте работать вместе и делать нашу
            компанию еще лучше!</p>
        <div class="col-sm-6">
            <form @submit.stop.prevent="sendIdea"
                  class="form-floating new-idea__form mb-3">
                <input type="text"
                       class="form-control"
                       v-model="messageTheme" />
                <label for="form-subject">Тема</label>
                <div class="invalid-feedback">
                    Обязательно укажите тему сообщения
                </div>

                <div class="form-floating  mb-3">
                    <textarea class="form-control"
                              placeholder="Добавьте сообщение"
                              style="height: 200px"
                              v-model="messageText"></textarea>
                    <label for="form-message">Сообщение</label>
                    <div class="invalid-feedback">
                        Это поле обязательно для заполнения
                    </div>
                </div>
                <div class="mb-3">
                    <label for="formFile"
                           class="form-label">Добавить файл</label>
                    <input class="form-control"
                           name="attachments-files"
                           type="file"
                           @change="handleMessageFileLoad">
                </div>
                <div class="mb-3">
                    <button class="btn btn-primary">
                        Отправить
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import Api from '@/utils/Api';
import { ref, type Ref, defineComponent } from 'vue';
export default defineComponent({
    setup() {
        const messageText: Ref<string> = ref('');
        const messageTheme: Ref<string> = ref('');
        const messageFile: Ref<File> = ref();

        const handleMessageFileLoad = (e: Event) => {
            const target = e?.target as HTMLInputElement
            if (!target || !target.files) return;
            messageFile.value = target.files[0];

        }


        const sendIdea = () => {
            const formData = new FormData();
            formData.append('messageTheme', messageTheme.value)
            formData.append('messageText', messageText.value)
            formData.append('messageFile', messageFile.value)
            console.log(messageFile.value)
            console.log('FormData содержит:');
            for (const [key, value] of formData.entries()) {
                console.log(key, value);
            }
            Api.post('ds', formData);
        }

        return {
            messageText,
            messageTheme,
            handleMessageFileLoad,
            sendIdea
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
</style>
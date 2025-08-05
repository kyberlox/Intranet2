<template>
    <div class="chatGpt">
        <h1 class="page__title">ChatGPT</h1>
        <div class="chatGpt__container">
            <div class="chatGpt__form-wrapper">
                <form class="chatGpt__form">
                    <div class="chatGpt__dialog-wrapper">
                        <div class="chatGpt__dialog"
                             v-for="(dialog, index) in dialogHistory"
                             :key="index">
                            <div class="chatGpt__dialog__message chatGpt__dialog__message-user p-3  rounded">
                                {{ dialog.user
                                }}</div>
                            <div
                                 class="chatGpt__dialog__message chatGpt__dialog__message-response  p-3  rounded assistant">
                                {{ dialog.response }}</div>
                        </div>
                    </div>

                    <div class="chatGpt__form-group">
                        <label>Роль собеседника</label>
                        <input v-model="role"
                               type="text"
                               placeholder="Укажите роль собеседника" />
                    </div>

                    <div class="chatGpt__form-group">
                        <label>Ваш запрос</label>
                        <textarea v-model="msgText"
                                  :rows="textAreaRowsToContent(msgText)"
                                  placeholder="Введите запрос..."></textarea>
                    </div>

                    <div class="chatGpt__form-group">
                        <button type="submit"
                                class="primary-button"
                                @click.prevent="sendToChatGpt">Отправить</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { textAreaRowsToContent } from "@/utils/StringUtils.js";
import { ref } from "vue";
import { defineComponent } from "vue";

export default defineComponent({
    name: "chatGpt",
    setup() {
        const role = ref("");
        const msgText = ref("");
        const sendToChatGpt = () => {
            fetch("https://gpt.emk.ru", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "role-assistant": "",
                    "role-system": role.value,
                    "role-user": msgText.value,
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    dialogHistory.value.push({
                        user: msgText.value,
                        response: data.choices[0].message.content
                    });
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
        };

        const dialogHistory = ref([{
            user: "Привет",
            response: "Привет! Как дела?"
        }]);

        return {
            role,
            msgText,
            textAreaRowsToContent,
            sendToChatGpt,
            dialogHistory
        };
    },
});
</script>
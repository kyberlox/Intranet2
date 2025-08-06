<template>
    <div class="neuroChat-page__wrapper">
        <div class="neuroChat-page">
            <NeuroChatSidebar :chatHistory="chatHistory"
                              :neuroModels="neuroModels" />
            <div class="neuroChat-content__wrapper">
                <div class="neuroChat-content">
                    <div class="neuroChat__messages__wrapper"
                         v-for="chat in messages"
                         :key="chat.user">
                        <div class="neuroChat__message neuroChat__message--user">
                            {{ chat.user }}
                        </div>
                        <div class="neuroChat__message neuroChat__message--neuro">
                            {{ chat.neuro }}
                        </div>
                    </div>
                </div>
                <div class="neuroChat__input-textarea__wrapper">
                    <div class="neuroChat__input-textarea">
                        <label>Введите сообщение</label>
                        <div class="neuroChat__input-container">
                            <textarea placeholder="Напишите ваше сообщение..."></textarea>
                            <button @click="isLoading = !isLoading"
                                    class="neuroChat__send-button pos-rel">
                                <svg v-if="!isLoading"
                                     width="20"
                                     height="20"
                                     viewBox="0 0 24 24"
                                     fill="none">
                                    <path d="M2 21L23 12L2 3V10L17 12L2 14V21Z"
                                          fill="currentColor" />
                                </svg>
                                <Loader v-else
                                        class="neuroChat__send-button__loader" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Loader from '@/components/layout/Loader.vue';
import NeuroChatSidebar from './components/NeuroChatSidebar.vue';

export default defineComponent({
    name: 'neuroChat',
    components: {
        NeuroChatSidebar,
        Loader
    },
    setup() {

        const chatHistory = [
            {
                theme: 'Привет'
            }
        ]

        const messages = [{
            user: 'Привет',
            neuro: 'Привет! Чем могу помочь?'
        }]

        const neuroModels = [{
            name: 'chatGpt',
            route: 'chatGpt'
        },
        {
            name: 'Deepseek',
            route: 'deepseek'
        }]

        const isLoading = ref(false);

        return {
            chatHistory,
            messages,
            neuroModels,
            isLoading
        }
    }
})
</script>
<template>
    <div class="neuroChat-page__wrapper">
        <div class="neuroChat-page">
            <NeuroChatSidebar :chatHistory="chatHistory"
                              :neuroModels="neuroModels"
                              @typeChanged="handleChatTypeChange" />
            <div class="neuroChat-content__wrapper">
                <div class="neuroChat-content">
                    <div v-if="chatDataToSend.length">
                        <div class="neuroChat__messages__wrapper"
                             v-for="(chat, index) in chatDataToSend"
                             :key="'chat' + index">
                            <div v-if="chat.role == 'user'"
                                 class="neuroChat__message neuroChat__message--user">
                                {{ chat.content }}
                            </div>
                            <div v-if="chat.role == 'assistant' && chatType == 'createImg' && chat.type == 'img'"
                                 class="neuroChat__messages">
                                <div class="neuroChat__message neuroChat__message--neuro">
                                    <img :src="chat.content" />
                                </div>
                                <div class="neuroChat__message neuroChat__message--link neuroChat__message--neuro">
                                    <a :href="chat.content"
                                       target="_blank">Открыть в новом окне</a>
                                </div>
                            </div>
                            <div v-else-if="chat.role == 'assistant'"
                                 class="neuroChat__message neuroChat__message--neuro"
                                 v-html="parseMarkdown(chat.content)">
                            </div>
                        </div>
                    </div>
                    <div v-else
                         class="neuroChat__message neuroChat__message--neuro">
                        {{ firstMessage }}
                    </div>
                </div>
                <div class="neuroChat__input-textarea__wrapper">
                    <div class="neuroChat__input-textarea">
                        <label>Введите сообщение</label>
                        <div class="neuroChat__input-container">
                            <div class="neuroChat__textarea__wrapper">
                                <textarea @keydown="handleKeyDown"
                                          v-model="userInput"
                                          placeholder="Напишите ваше сообщение..."></textarea>
                                <button @click="sendMsg"
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
                            <div class="neuroChat__file-upload"
                                 v-if="chatType == 'textChat'">
                                <input type="file"
                                       ref="fileInputNode"
                                       @change="handleFileSelect"
                                       class="neuroChat__file-input"
                                       accept=".pdf,.doc,.docx,.txt,.jpg,.png" />
                                <div class="neuroChat__add-file"
                                     @click="triggerFileSelect">
                                    <AddFileIcon />
                                </div>
                                <p class="fs-s">{{ fileToUploadName }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import Loader from '@/components/layout/Loader.vue';
import NeuroChatSidebar from './components/NeuroChatSidebar.vue';
import Api from '@/utils/Api';
import { handleApiError } from '@/utils/ApiResponseCheck';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import AddFileIcon from '@/assets/icons/AddFileIcon.svg?component';
import type { INeuroChat } from '@/interfaces/IEntities';
import { parseMarkdown } from '@/utils/parseMarkdown';

export type IChatType = "textChat" | "createImg";

export default defineComponent({
    name: 'neuroChat',
    components: {
        NeuroChatSidebar,
        Loader,
        AddFileIcon
    },
    setup() {
        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);
        const fileToUploadName = ref<string>()
        const chatHistory = ref();
        const firstMessage = ref();
        const analyzeMessage = ref(false);

        const neuroModels: { name: string, type: IChatType }[] = [{
            name: 'Чат',
            type: 'textChat'
        },
        {
            name: 'Генерация изображений',
            type: 'createImg'
        },]

        const isLoading = ref(false);
        const userInput = ref('');
        const fileInputNode = ref<HTMLInputElement>();
        const fileInput = ref<File>();
        const chatDataToSend = ref<INeuroChat[]>([]);

        const createImageChatData = ref();
        const analyzeImageChatData = ref();
        const chatType = ref<IChatType>();

        const handleFileSelect = (event: Event) => {
            const target = event.target as HTMLInputElement;
            const file = target.files;
            if (file?.length) {
                fileToUploadName.value = file[0].name;
            }
        }
        const triggerFileSelect = () => {
            fileInputNode.value?.click();
        }

        watch((fileInput), () => {
            if (fileInput.value) {
                analyzeMessage.value = true;
            }
            else analyzeMessage.value = false;
        })

        const chatWindowUpdate = () => {
            isLoading.value = true;
            if (chatType.value == 'textChat') {
                if (!chatDataToSend.value.find((e) => e.role == 'system')) {
                    chatDataToSend.value.push({ 'role': 'system', content: 'Определи из контекста, отвечай на русском' });
                }
                if (analyzeMessage.value) {
                    analyzeImageChatData.value.push({ 'role': 'user', content: userInput.value })
                } else
                    chatDataToSend.value.push({ 'role': 'user', content: userInput.value });
            }
            else if (chatType.value == 'createImg') {
                createImageChatData.value = {
                    prompt: userInput.value,
                    size: '1024x1024',
                    quality: 'standard',
                    style: 'vivid'
                }
            }
        }

        const sendMsg = async () => {
            chatWindowUpdate();
            if (chatType.value == 'textChat') {
                if (analyzeMessage.value) {
                    await Api.postVendor('https://gpt.emk.ru/analyze-image', analyzeImageChatData.value)
                        .then((data) => {
                            chatDataToSend.value.push({
                                role: 'assistant',
                                content: data.image_url,
                                type: 'img'
                            })
                        })
                        .catch((error) => {
                            handleApiError(error, toast)
                        })
                        .finally(() => {
                            isLoading.value = false;
                            userInput.value = '';

                        })
                }
                else
                    await Api.postVendor('https://gpt.emk.ru/dialog', chatDataToSend.value)
                        .then((data) => {
                            chatDataToSend.value = data
                        })
                        .catch((error) => {
                            handleApiError(error, toast)
                        })
                        .finally(() => {
                            isLoading.value = false;
                            userInput.value = '';

                        })
            }
            else if (chatType.value == 'createImg') {
                chatDataToSend.value.length = 0;
                chatDataToSend.value.push({
                    role: 'user',
                    content: userInput.value,
                })
                await Api.postVendor('https://gpt.emk.ru/generate-image', createImageChatData.value)
                    .then((data) => {
                        chatDataToSend.value.push({
                            role: 'assistant',
                            content: data.image_url,
                            type: 'img'
                        })
                    })
                    .catch((error) => {
                        handleApiError(error, toast)
                    })
                    .finally(() => {
                        isLoading.value = false;
                        userInput.value = '';

                    })
            }
        }

        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                if (userInput.value.trim() && !isLoading.value) {
                    sendMsg();
                    userInput.value = '';
                }
            }
        }

        const handleChatTypeChange = (type: IChatType) => {
            fileInput.value = undefined;
            fileToUploadName.value = '';
            chatDataToSend.value.length = 0;
            chatType.value = type;
            firstMessage.value = type == 'createImg' ? 'Привет! Опиши изображение, которое хочешь получить' : 'Привет! Чем могу помочь?'
        }

        return {
            chatHistory,
            neuroModels,
            isLoading,
            userInput,
            fileInputNode,
            fileToUploadName,
            chatDataToSend,
            chatType,
            firstMessage,
            handleChatTypeChange,
            parseMarkdown,
            sendMsg,
            handleFileSelect,
            triggerFileSelect,
            handleKeyDown
        }
    }
})
</script>
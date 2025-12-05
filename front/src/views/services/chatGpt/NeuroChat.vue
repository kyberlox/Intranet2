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
                                   accept=".pdf,.doc,.docx,.txt,.jpg,.png"
                                   multiple />
                            <div class="neuroChat__add-file"
                                 @click="triggerFileSelect">
                                <AddFileIcon />
                            </div>
                            <div class="neuroChat__file-list">
                                <p v-for="(file, index) in filesToUpload"
                                   :key="index"
                                   class="fs-s neuroChat__file-item">
                                    {{ file.name }}
                                    <span class="neuroChat__remove-file"
                                          @click="removeFile(index)">×</span>
                                </p>
                            </div>
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
import { handleApiError } from '@/utils/apiResponseCheck';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import AddFileIcon from '@/assets/icons/AddFileIcon.svg?component';
import type { INeuroChat } from '@/interfaces/IEntities';
import { parseMarkdown } from '@/utils/parseMarkdown';

export type IChatType = "textChat" | "createImg";

interface IUploadFile {
    file: File;
    name: string;
}

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
        const filesToUpload = ref<IUploadFile[]>([]);
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
        const chatDataToSend = ref<INeuroChat[]>([]);

        const createImageChatData = ref();
        const analyzeImageChatData = ref<INeuroChat[]>([]);
        const chatType = ref<IChatType>();

        const handleFileSelect = (event: Event) => {
            const target = event.target as HTMLInputElement;
            const selectedFiles = target.files;

            if (selectedFiles?.length) {
                for (let i = 0; i < selectedFiles.length; i++) {
                    const file = selectedFiles[i];
                    filesToUpload.value.push({
                        file: file,
                        name: file.name
                    });
                }

                if (fileInputNode.value) {
                    fileInputNode.value.value = '';
                }
            }
        }

        const removeFile = (index: number) => {
            filesToUpload.value.splice(index, 1);
        }

        const triggerFileSelect = () => {
            fileInputNode.value?.click();
        }

        watch(() => filesToUpload.value.length, (newLength) => {
            analyzeMessage.value = newLength > 0;
        }, { immediate: true })

        const chatWindowUpdate = () => {
            isLoading.value = true;
            if (chatType.value == 'textChat') {
                if (!chatDataToSend.value.find((e) => e.role == 'system')) {
                    chatDataToSend.value.push({ 'role': 'system', content: 'Определи из контекста, отвечай на русском' });
                }
                if (analyzeMessage.value) {
                    analyzeImageChatData.value.push({ 'role': 'user', content: userInput.value })
                } else {
                    chatDataToSend.value.push({ 'role': 'user', content: userInput.value });
                }
            }
            else if (chatType.value == 'createImg') {
                createImageChatData.value = {
                    prompt: userInput.value,
                    size: '1024x1024',
                    quality: 'standard',
                    style: 'vivid'
                }
            }
            userInput.value = ''
        }

        const sendMsg = async () => {
            chatWindowUpdate();
            if (chatType.value == 'textChat') {
                if (analyzeMessage.value) {
                    const formData = new FormData();

                    filesToUpload.value.forEach((fileObj, index) => {
                        formData.append(`files`, fileObj.file);
                    });

                    const newUserMsg = analyzeImageChatData.value[analyzeImageChatData.value.length - 1].content;
                    formData.append('data', JSON.stringify({ prompt: newUserMsg }));
                    chatDataToSend.value.push({
                        role: 'user',
                        content: newUserMsg,
                    })
                    formData.getAll('files').forEach((e) => {
                        chatDataToSend.value.push({
                            role: 'user',
                            content: (e as File).name
                        })
                    })
                    filesToUpload.value = [];
                    await Api.postVendor('https://gpt.emk.ru/analyze-files', formData)
                        .then((data) => {
                            chatDataToSend.value.push({
                                role: 'assistant',
                                content: data.analysis
                            })
                        })
                        .catch((error) => {
                            handleApiError(error, toast)
                        })
                        .finally(() => {
                            isLoading.value = false;
                        })
                }
                else {
                    await Api.postVendor('https://gpt.emk.ru/dialog', chatDataToSend.value)
                        .then((data) => {
                            chatDataToSend.value = data
                        })
                        .catch((error) => {
                            handleApiError(error, toast)
                        })
                        .finally(() => {
                            isLoading.value = false;
                        })
                }
            }
            else if (chatType.value == 'createImg') {
                chatDataToSend.value.length = 0;
                chatDataToSend.value.push({
                    role: 'user',
                    content: createImageChatData.value.prompt,
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
                    })
            }
        }

        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                if (userInput.value.trim() && !isLoading.value) {
                    sendMsg();
                }
            }
        }

        const handleChatTypeChange = (type: IChatType) => {
            filesToUpload.value = [];
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
            filesToUpload,
            chatDataToSend,
            chatType,
            firstMessage,
            handleChatTypeChange,
            parseMarkdown,
            sendMsg,
            handleFileSelect,
            removeFile,
            triggerFileSelect,
            handleKeyDown
        }
    }
})
</script>
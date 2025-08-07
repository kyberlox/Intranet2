<template>
    <div class="neuroChat-page__wrapper">
        <div class="neuroChat-page">
            <NeuroChatSidebar :chatHistory="chatHistory"
                              :neuroModels="neuroModels" />
            <div class="neuroChat-content__wrapper">
                <div class="neuroChat-content">
                    <div class="neuroChat__messages__wrapper"
                         v-if="chatDataToSend.length"
                         v-for="(chat, index) in chatDataToSend"
                         :key="'chat' + index">
                        <div v-if="chat.role == 'user'"
                             class="neuroChat__message neuroChat__message--user">
                            {{ chat.content }}
                        </div>
                        <div v-if="chat.role == 'assistant'"
                             class="neuroChat__message neuroChat__message--neuro">
                            {{ chat.content }}
                        </div>
                    </div>
                    <div v-else
                         class="neuroChat__message neuroChat__message--neuro">
                        Привет! Чем могу помочь?
                    </div>
                </div>
                <div class="neuroChat__input-textarea__wrapper">
                    <div class="neuroChat__input-textarea">
                        <label>Введите сообщение</label>
                        <div class="neuroChat__input-container">
                            <div class="neuroChat__textarea__wrapper">
                                <textarea v-model="userInput"
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
                            <div class="neuroChat__file-upload">
                                <input type="file"
                                       ref="fileInputNode"
                                       @change="handleFileSelect"
                                       class="neuroChat__file-input"
                                       accept=".pdf,.doc,.docx,.txt,.jpg,.png">
                                <div class="neuroChat__add-file"
                                     @click="triggerFileSelect">
                                    <AddFileIcon />
                                </div>
                                </input>
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
import { defineComponent, ref, type Ref } from 'vue';
import Loader from '@/components/layout/Loader.vue';
import NeuroChatSidebar from './components/NeuroChatSidebar.vue';
import Api from '@/utils/Api';
import { handleApiError } from '@/utils/ApiResponseCheck';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import AddFileIcon from '@/assets/icons/AddFileIcon.svg?component';
import type { INeuroChat } from '@/interfaces/entities/INeuroChat';

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

        const neuroModels = [{
            name: 'chatGpt',
            route: 'chatGpt'
        },
        {
            name: 'Deepseek',
            route: 'deepseek'
        }]

        const isLoading = ref(false);
        const userInput = ref('');
        const fileInputNode = ref<HTMLInputElement>();
        const fileInput = ref<File>();
        const chatDataToSend = ref<INeuroChat[]>([]);

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

        const sendMsg = async () => {
            isLoading.value = true;
            if (!chatDataToSend.value.find((e) => e.role == 'system')) {
                chatDataToSend.value.push({ 'role': 'system', content: 'Определи из контекста, отвечай на русском' });
            }
            chatDataToSend.value.push({ 'role': 'user', content: userInput.value });
            userInput.value = '';

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

        return {
            chatHistory,
            neuroModels,
            isLoading,
            userInput,
            fileInputNode,
            fileToUploadName,
            chatDataToSend,
            sendMsg,
            handleFileSelect,
            triggerFileSelect
        }
    }
})
</script>
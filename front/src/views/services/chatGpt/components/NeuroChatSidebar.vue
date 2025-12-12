<template>
<div class="neuroChat-sidebar">
    <div class="neuroChat-sidebar__model-select__wrapper">
        <div class="neuroChat-sidebar__model-select">
            <select v-model="chatType">
                <option v-for="model in neuroModels"
                        :key="model.type"
                        :value="model.type">
                    {{ model.name }}
                </option>
            </select>
        </div>
        <!-- <div class="neuroChat-sidebar__new-chat-button">
                <button>Создать +</button>
            </div> -->
    </div>
    <div class="neuroChat-sidebar__history__wrapper"
         v-if="chatHistory?.length">
        <div class="neuroChat-sidebar__history">
            <div class="neuroChat-sidebar__history-title">История сообщений</div>
            <div class="neuroChat-sidebar__history__item"
                 v-for="item in chatHistory"
                 :key="item.theme">
                {{ item.theme }}
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';

interface INeuroModels {
    type: 'textChat' | 'createImg',
    name: string
}

interface IChatHistory {
    theme: string
}

export default defineComponent({
    name: 'neuroSidebar',
    props: {
        neuroModels: Array<INeuroModels>,
        chatHistory: Array<IChatHistory>
    },
    setup(props, { emit }) {
        const chatType = ref<'textChat' | 'createImg'>('textChat');

        watch((chatType), () => {
            emit('typeChanged', chatType.value)
        }, { immediate: true })

        return {
            chatType,
        }
    }
})
</script>
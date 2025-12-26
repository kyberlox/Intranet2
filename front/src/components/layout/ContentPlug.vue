<template>
<div class="empty-page-plug__wrapper">
    <div class="empty-page-plug__title">
        <div v-html="currentPlug">
        </div>
    </div>
    <div class="empty-page-plug__img__wrapper">
        <img class="empty-page-plug__img"
             :src=plugImg>
        <span class="empty-page-plug__img__mark"
              v-if="needGptMark">
            *изображение сгенерировано сервисом
            <span class="orange">chatGPT</span> внутри корпоративного портала</span>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
    props: {
        needGptMark: {
            type: Boolean,
            default: () => true
        },
        plugText: {
            type: String,
        },
        plugImg: {
            type: String,
            required: true
        }
    },
    setup(props) {
        const currentPlug = ref(props.plugText);

        return {
            currentPlug
        }
    }
})
</script>
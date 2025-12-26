<template>
<div class="empty-page-plug__wrapper">
    <div class="empty-page-plug__title">
        <div v-html="currentPlug">
        </div>
    </div>
    <div class="empty-page-plug__img__wrapper">
        <img class="empty-page-plug__img"
             :src=plugImage>
        <span class="empty-page-plug__img__mark"
              v-if="needGptMark">
            *изображение сгенерировано сервисом
            <span class="orange">chatGPT</span> внутри корпоративного портала</span>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import plugImage from '@/assets/imgs/plugs/empty.jpg'

export default defineComponent({
    props: {
        needGptMark: {
            type: Boolean,
            default: () => true
        },
        plugText: {
            type: String,
        }
    },
    setup(props) {
        const currentPlug = ref(props.plugText);

        return {
            plugImage,
            currentPlug
        }
    }
})
</script>
<template>
<div class="empty-page-plug__wrapper">
    <div class="empty-page-plug__title">
        <div>
            <span class="orange">
                Тут пока пусто.
            </span>
            <span>
                Следите за обновлениями</span>
        </div>
    </div>
    <div class="empty-page-plug__img__wrapper">
        <img class="empty-page-plug__img"
             :src=plug>
        <span class="empty-page-plug__img__mark">
            *изображение сгенерировано сервисом
            <span class="orange">chatGPT</span> внутри корпоративного портала</span>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import plug from '@/assets/imgs/plugs/empty.jpg'
export default defineComponent({
    setup() {
        return {
            plug
        }
    }
})
</script>
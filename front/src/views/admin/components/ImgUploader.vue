<template>
    <div class="card">
        <FileUpload name="demo[]"
                    url="/api/upload"
                    @upload="onAdvancedUpload()"
                    :multiple="true"
                    accept="image/*"
                    :maxFileSize="1000000">
            <template #empty>
                <span class="drag-n-drop__text">Перетащите изображения в эту область либо загрузите по кнопке</span>
            </template>
        </FileUpload>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    setup() {
        const onAdvancedUpload = () => {
        };
        return {
            onAdvancedUpload
        }
    }
})
</script>
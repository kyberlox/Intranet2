<template>
<Editor :modules="editorModules"
        editorStyle="height: 350px"
        @text-change="handleTextChange">
    <template v-slot:toolbar>
        <span class="ql-formats"></span>
    </template>
</Editor>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Editor from 'primevue/editor';
import sanitizeHtml from 'sanitize-html';

export default defineComponent({
    components: {
        Editor
    },
    emits: ['update:modelValue', 'paste'],
    setup(props, { emit }) {
        const content = ref('');

        // Автоматически очищаем при любом изменении текста
        const handleTextChange = ({ htmlValue }: { htmlValue: string }) => {
            if (htmlValue) {
                // Автоматически применяем sanitize-html
                const cleanHtml = sanitizeHtml(htmlValue, {
                    allowedAttributes: {},
                    allowedStyles: {},
                    transformTags: {
                        'span': () => ({ tagName: '', attribs: {} })
                    }
                }).replaceAll('&nbsp;', ' ');

                // Если HTML изменился после очистки
                if (cleanHtml !== htmlValue) {
                    // Обновляем содержимое редактора
                    // Через ref или другим способом

                    emit('update:modelValue', cleanHtml.replaceAll('&nbsp;', ' '));
                }
                console.log(htmlValue);
            }
        };

        const editorModules = {
            toolbar: [
                ['bold', 'italic', 'underline'],
                [{ 'color': [] }],
                [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                ['link']
            ],
            clipboard: {
                matchVisual: false,
            }
        };

        return {
            content,
            editorModules,
            handleTextChange
        };
    }
});
</script>
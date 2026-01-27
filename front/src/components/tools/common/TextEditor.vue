<template>
<Editor :modules="editorModules"
        v-model="content"
        editorStyle="height: 350px"
        @text-change="handleTextChange">
    <template v-slot:toolbar>
        <span class="ql-formats"></span>
    </template>
</Editor>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import Editor from 'primevue/editor';
import sanitizeHtml from 'sanitize-html';

export default defineComponent({
    name: 'TextEditor',
    components: {
        Editor
    },
    props: {
        modelValue: {
            type: String,
            default: ''
        }
    },
    emits: ['update:modelValue', 'paste'],
    setup(props, { emit }) {
        const content = ref(props.modelValue);

        watch(() => props.modelValue, (newValue) => {
            if (newValue !== content.value) {
                content.value = sanitizeValue(newValue);
            }
        }, { immediate: true, deep: true });

        const sanitizeValue = (html: string): string => {
            if (!html) return '';

            let cleanHtml = sanitizeHtml(html, {
                allowedTags: ['b', 'i', 'u', 'strong', 'em', 'a', 'p', 'br', 'li', 'ol', 'ul'],
                allowedAttributes: {
                    'a': ['href', 'target', 'rel']
                },
                allowedStyles: {},
                transformTags: {
                    'div': 'p',
                    'span': () => ({ tagName: '', attribs: {} })
                },
                disallowedTagsMode: 'discard'
            }).replaceAll('&nbsp;', ' ');

            cleanHtml = cleanHtml.replace(/<li>\s*<ul/g, '<ul');
            cleanHtml = cleanHtml.replace(/<li>\s*<ol/g, '<ol');
            cleanHtml = cleanHtml.replace(/<\/ol>\s*<\/li>/g, '</ol>');

            return cleanHtml;
        };

        const handleTextChange = ({ htmlValue }: { htmlValue: string }) => {
            if (htmlValue !== undefined) {
                const cleanHtml = sanitizeValue(htmlValue);
                content.value = cleanHtml;
                emit('update:modelValue', cleanHtml);
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
            handleTextChange,
        };
    }
});
</script>
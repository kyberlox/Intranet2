<template>
    <Editor v-model="editorValue"
            :modules="editorModules"
            editorStyle="height: 350px">
        <template v-slot:toolbar>
            <span class="ql-formats"></span>
        </template>
    </Editor>
</template>


<script lang="ts">
import { defineComponent, ref, watchEffect } from 'vue';
import Editor from 'primevue/editor';

export default defineComponent({
    components: {
        Editor
    },
    setup() {
        const editorValue = ref();

        watchEffect(() => console.log(editorValue.value))


        const editorModules = {
            toolbar: [
                ['bold', 'italic', 'underline'],
                [{ 'color': [] }],
                [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                [{ 'align': [] }],
                ['link', 'image']
            ]
        };

        return {
            editorValue,
            editorModules
        };
    }
});
</script>
<style>
.ql-snow .ql-tooltip[data-mode='link']::before {
    content: 'url:' !important;
}

.ql-snow .ql-tooltip.ql-editing a.ql-action::after {
    content: 'Далее' !important;
}
</style>
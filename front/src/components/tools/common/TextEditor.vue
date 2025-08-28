<template>
    <Editor :modules="editorModules"
            editorStyle="height: 350px">
        <template v-slot:toolbar>
            <span class="ql-formats"></span>
        </template>
    </Editor>
</template>


<script lang="ts">
import { defineComponent } from 'vue';
import Editor from 'primevue/editor';

export default defineComponent({
    components: {
        Editor
    },
    setup() {
        const editorModules = {
            toolbar: [
                ['bold', 'italic', 'underline'],
                [{ 'color': [] }],
                [{ 'list': 'ordered' }, { 'list': 'bullet' }],

                ['link']
            ]
        };

        return {
            editorModules
        };
    }
});
</script>
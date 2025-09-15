<template>
    <ModeratorValidationPanel :isModer="false" />
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ModeratorValidationPanel from '../moderatorPanel/ModeratorValidationPanel.vue';

export default defineComponent({
    components: {
        ModeratorValidationPanel
    },
    setup() {
        return {

        }
    }
})
</script>

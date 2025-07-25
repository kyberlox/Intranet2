<template>
    <div class="admin-element-inner__field-content">
        <p class="admin-element-inner__field-title">{{ item?.name }}</p>
        <TextEditor class="admin-element-inner__text-editor"
                    v-model="value"
                    @vue:updated="handleValuePick" />
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from 'vue';
import TextEditor from './TextEditor.vue';
import type { IAdminListItem } from '@/interfaces/entities/IAdmin';


export default defineComponent({
    components: {
        TextEditor
    },
    props: {
        item: {
            type: Object as PropType<IAdminListItem>
        },
        inputValue: {
            type: String
        }
    },
    setup(props, { emit }) {
        const value = ref(props.inputValue);
        return {
            value,
            handleValuePick: () => emit('pick', value.value)
        }
    }
})
</script>
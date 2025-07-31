<template>
    <div class="admin-element-inner__field-content">
        <p class="admin-element-inner__field-title fs-l">{{ item?.name }}</p>
        <TextEditor class="admin-element-inner__text-editor fs-m"
                    v-model="value"
                    @vue:mounted="handleValuePick"
                    @vue:updated="handleValuePick" />
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from 'vue';
import TextEditor from './TextEditor.vue';
import type { IAdminListItem } from '@/interfaces/entities/IAdmin';
import { parseMarkdown } from '@/utils/useMarkdown';

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
        const value = ref(props.item?.value);
        return {
            value,
            handleValuePick: () => emit('pick', value.value?.replaceAll('&nbsp;', ' ')),
            parseMarkdown
        }
    }
})
</script>
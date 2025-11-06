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
import { defineComponent, type PropType, ref, watch } from 'vue';
import TextEditor from '@/components/tools/common/TextEditor.vue';
import type { IAdminListItem } from '@/interfaces/IEntities';
import { parseMarkdown } from '@/utils/parseMarkdown';

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
        const value = ref<string>();

        watch((props), () => {
            if (!props.item?.value) return
            value.value = String(props.item?.value)
        }, { immediate: true, deep: true })

        return {
            value,
            handleValuePick: () => emit('pick', (value.value as string)?.replaceAll('&nbsp;', ' ')),
            parseMarkdown
        }
    }
})
</script>
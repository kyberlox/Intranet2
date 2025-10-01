<template>
<div class="admin-element-inner__field-content">
    <p v-if="item?.name"
       class="admin-element-inner__field-title fs-l">{{ item?.name }}</p>
    <select class="admin-element-inner__select"
            @change="handleValuePick"
            v-model="value">
        <option class="admin-element-inner__select-option"
                v-for="(option, index) in item?.values"
                :value="typeof option === 'string' || typeof option === 'boolean' ? option : option.id"
                :key=index>
            {{ (typeof option === 'string' || typeof option === 'boolean' ? (yesOrNoFormat ?
                renderOptionText(option) : option) : option.name) }}
        </option>
    </select>
</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, type PropType, ref } from 'vue';
import type { IAdminListItem } from '@/interfaces/IEntities';

export default defineComponent({
    name: 'SelectComponent',
    props: {
        yesOrNoFormat: {
            type: Boolean,
            default: true
        },
        item: {
            type: Object as PropType<IAdminListItem>
        },
    },
    setup(props, { emit }) {
        const value = ref(props.item?.value);
        onMounted(() => emit('pick', value.value))
        return {
            value,
            renderOptionText: (text: boolean | string) => { return (String(text) == 'true' ? 'Да' : 'Нет') },
            handleValuePick: () => { emit('pick', value.value) }
        }
    }
})
</script>
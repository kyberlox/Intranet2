<template>
<div class="admin-element-inner__field-content">
    <p v-if="item?.name"
       class="admin-element-inner__field-title fs-l">{{ item?.name }}</p>
    <input class="admin-element-inner__input fs-m"
           v-model="value"
           @input="handleValuePick"
           :type="type"
           :disabled="Boolean(item?.disabled)"
           :placeholder="placeholder" />
</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, type PropType, ref } from 'vue';
import type { IAdminListItem } from '@/interfaces/IEntities';

export default defineComponent({
    props: {
        item: {
            type: Object as PropType<IAdminListItem>
        },
        placeholder: {
            type: String
        },
        type: {
            type: String,
            default: () => 'text'
        }
    },
    setup(props, { emit }) {
        const value = ref(props.item?.value);
        const handleValuePick = () => { emit('pick', value.value) };

        onMounted(() => {
            handleValuePick();
        })

        return {
            value,
            handleValuePick
        }
    }
})
</script>
<template>
    <div class="admin-element-inner__field-content">
        <p class="admin-element-inner__field-title fs-l">{{ item?.name }}</p>
        <input class="admin-element-inner__input fs-m"
               v-model="value"
               @input="handleValuePick"
               :disabled="Boolean(item?.disabled)" />
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from 'vue';
import type { IAdminListItem } from '@/interfaces/entities/IAdmin';


export default defineComponent({
    props: {
        item: {
            type: Object as PropType<IAdminListItem>
        },
    },
    setup(props, { emit }) {
        const value = ref(props.item?.value);
        return {
            value,
            handleValuePick: () => emit('pick', value.value)
        }
    }
})
</script>
<template>
    <div class="admin-element-inner__field-content">
        <p class="admin-element-inner__field-title">{{ item?.name }}</p>
        <select class="admin-element-inner__select"
                @change="handleValuePick"
                v-model="value">
            <option class="admin-element-inner__select-option"
                    v-for="(option, index) in item?.values"
                    :key=index>
                {{ option }}
            </option>
        </select>
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
        const value = ref();
        return {
            value,
            handleValuePick: () => emit('pick', value.value)
        }
    }
})
</script>
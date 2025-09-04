<template>
    <div class="admin-element-inner__field-content">
        <p class="admin-element-inner__field-title fs-l">{{ item?.name }}</p>
        <input class="admin-element-inner__input fs-m"
               v-model="value"
               @input="handleValuePick"
               :type="'text'"
               :disabled="Boolean(item?.disabled)"
               :placeholder="placeholder" />
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, type PropType, ref } from 'vue';
import type { IAdminListItem } from '@/interfaces/entities/IAdmin';


export default defineComponent({
    props: {
        item: {
            type: Object as PropType<IAdminListItem>
        },
        placeholder: {
            type: String
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
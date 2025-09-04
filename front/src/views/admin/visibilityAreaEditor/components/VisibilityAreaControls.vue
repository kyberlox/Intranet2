<template>
    <div class="visibility-editor__area-users__edit-methods">
        <button @click="()=>changeEditMode"
                class="visibility-editor__area-users__edit-methods__add primary-button">
            {{ buttonText }}
        </button>
        <!-- <AdminEditInput class="visibility-editor__area-users__edit-methods__search"
                                :item="{ name: '', value: '' }"
                                :placeholder="'Фильтр по фио'" /> -->
    </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import AdminEditInput from '@/views/admin/components/inputFields/AdminEditInput.vue';

export default defineComponent({
    props: {
        editGroupMode: {
            type: Boolean
        }
    },
    emits: ['changeEditMode'],
    components: {
        AdminEditInput
    },
    setup(props, { emit }) {

        return {
            buttonText: computed(() => props.editGroupMode ? 'Вернуться' : 'Изменить'),
            changeEditMode: (value: boolean) => emit('changeEditMode', value),
        }
    }
})
</script>
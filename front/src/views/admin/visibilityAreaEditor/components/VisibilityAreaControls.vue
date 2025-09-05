<template>
    <div class="visibility-editor__area-users__edit-methods">
        <button @click="changeEditMode"
                class="visibility-editor__area-users__edit-methods__add primary-button">
            {{ buttonText }}
        </button>
        <div class="visibility-editor__area-users__edit-methods__input-wrapper"
             v-if="editGroupMode">
            <AdminEditInput class="visibility-editor__area-users__edit-methods__search"
                            :item="{ name: '', value: '' }"
                            @pick="(abob: string) => console.log(abob)"
                            :placeholder="'Фильтр по подразделению'" />

            <AdminEditInput class="visibility-editor__area-users__edit-methods__search"
                            :item="{ name: '', value: '' }"
                            @pick="(abob: string) => console.log(abob)"
                            :placeholder="'Фильтр по фио'" />
        </div>
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
            buttonText: computed(() => props.editGroupMode ? 'Вернуться' : 'Добавить'),
            changeEditMode: () => emit('changeEditMode', !props.editGroupMode),
        }
    }
})
</script>
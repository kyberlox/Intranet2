<template>
    <div class="visibility-editor__area-users__edit-methods">
        <button @click="changeEditMode"
                class="visibility-editor__area-users__edit-methods__add primary-button">
            {{ buttonText }}
        </button>
        <div class="visibility-editor__area-users__edit-methods__input-wrapper">

            <AdminEditInput class="visibility-editor__area-users__edit-methods__search"
                            :class="{ 'disabled visibility-editor__area-users__edit-methods__search--disabled': fioFilter }"
                            :item="{ name: '', value: depFilter }"
                            @pick="(inputValue: string) => handleInputFilter(inputValue, 'dep')"
                            :placeholder="'Поиск по подразделениям'" />

            <AdminEditInput class="visibility-editor__area-users__edit-methods__search"
                            :class="{ 'disabled visibility-editor__area-users__edit-methods__search--disabled': depFilter }"
                            :item="{ name: '', value: fioFilter }"
                            @pick="(inputValue: string) => handleInputFilter(inputValue, 'fio')"
                            :placeholder="'Поиск по фио'" />

        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref } from 'vue';
import AdminEditInput from '@/views/admin/components/inputFields/AdminEditInput.vue';

export default defineComponent({
    props: {
        editGroupMode: {
            type: Boolean
        }
    },
    emits: ['changeEditMode', 'depFilterChanged', 'fioFilterChanged'],
    components: {
        AdminEditInput
    },
    setup(props, { emit }) {
        const fioFilter = ref<string>();
        const depFilter = ref<string>();

        const handleInputFilter = (value: string, type: 'dep' | 'fio') => {
            switch (type) {
                case 'fio':
                    fioFilter.value = value;
                    depFilter.value = '';
                    emit('fioFilterChanged', fioFilter.value)
                    break;
                case 'dep':
                    fioFilter.value = '';
                    depFilter.value = value;
                    emit('depFilterChanged', depFilter.value)
                default:
                    break;
            }
        }

        return {
            fioFilter,
            depFilter,
            buttonText: computed(() => props.editGroupMode ? 'Вернуться' : 'Добавить'),
            handleInputFilter,
            changeEditMode: () => emit('changeEditMode', !props.editGroupMode),
        }
    }
})
</script>
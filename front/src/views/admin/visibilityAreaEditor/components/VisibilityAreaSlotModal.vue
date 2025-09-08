<template>
    <div class="visibility-editor__add-new-area__slot">
        <AdminEditInput @pick="(value: string) => newAreaName = value"
                        :placeholder="'Введите название области видимости'" />
        <div class="visibility-editor__add-new-area__slot__buttons">
            <div class="primary-button visibility-editor__add-new-area__slot__button visibility-editor__add-new-area__slot__button--cancel"
                 @click="cancelArea">
                <CancelIcon />
            </div>
            <div class="primary-button visibility-editor__add-new-area__slot__button visibility-editor__add-new-area__slot__button--accept"
                 :class="{ 'visibility-editor__add-new-area__slot__button--disabled': !newAreaName }"
                 @click="acceptArea">
                <CheckIcon />
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import AdminEditInput from '../../components/inputFields/AdminEditInput.vue';
import CheckIcon from '@/assets/icons/common/Check.svg?component';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';

export default defineComponent({
    components: {
        AdminEditInput,
        CheckIcon,
        CancelIcon
    },
    emits: ['cancelArea', 'acceptArea'],
    setup(props, { emit }) {
        const newAreaName = ref<string>();

        return {
            newAreaName,
            cancelArea: () => emit('cancelArea'),
            acceptArea: () => newAreaName.value ? emit('acceptArea', newAreaName.value) : ''
        }
    }
})
</script>
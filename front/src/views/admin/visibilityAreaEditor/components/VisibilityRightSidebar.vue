<template>
    <div class="visibility-editor__right-sidebar">
        <div>
            <table>
                <tbody>
                    <tr class="user-choices-table__row"
                        v-for="choice in choices"
                        :key="choice.type + choice.id">
                        <td>{{ choice.name }}</td>
                    </tr>
                </tbody>
            </table>
            <div v-if="editMode"
                 class="visibility-editor__button-group mt20">
                <button class='primary-button'
                        @click="$emit('saveChoices')">Сохранить</button>
                <button class='primary-button'
                        @click="$emit('clearChoices')">Сбросить</button>
            </div>
            <button v-else-if="choices?.length"
                    class='primary-button mt20'
                    @click="$emit('deleteMultipleUsers')">
                Удалить
            </button>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { type IChoice } from '@/interfaces/IEntities';
export default defineComponent({
    props: {
        choices: {
            type: Array<IChoice>
        },
        editMode: {
            type: Boolean
        }
    },
    emits: ['saveChoices', 'clearChoices', 'deleteMultipleUsers'],
    setup(props, { emit }) {
        return {

        }
    }
})
</script>
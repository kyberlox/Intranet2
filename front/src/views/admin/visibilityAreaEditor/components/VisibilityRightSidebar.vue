<template>
    <div class="visibility-editor__right-sidebar">
        <table>
            <tbody>
                <tr v-for="choice in choices"
                    :key="choice.type + choice.id">
                    <td>{{ choice.name }}</td>
                </tr>
            </tbody>
        </table>
        <div class="visibility-editor__button-group">
            <button class='primary-button'
                    @click="$emit('saveChoices')">Сохранить</button>
            <button class='primary-button'
                    @click="$emit('clearChoices')">Сбросить</button>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { type IChoice } from '../VisibilityAreaEditor.vue';
export default defineComponent({
    props: {
        choices: {
            type: Array<IChoice>
        }
    },
    emits: ['saveChoices', 'clearChoices'],
    setup(props, { emit }) {
        return {

        }
    }
})
</script>
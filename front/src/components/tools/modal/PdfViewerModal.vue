<template>
<div class="modal modal--fullscreen modal--gazette fade show"
     style="display: block;">
    <div class="modal-dialog modal-fullscreen">
        <div class="modal-content modal__content--fullscreen modal__content--pdf">
            <div class="modal-header">
                <h1 class="modal-title fs-5">{{ activeGazete.name ?? 'Корпоративная газета' }}</h1>
                <button @click="closeModal"
                        type="button"
                        class="btn-close mr10"></button>
            </div>
            <div class="modal-body">
                <object :data='activeGazete.indirect_data.pdf'></object>
            </div>
            <div class="modal-footer">
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    props: {
        activeGazete: {
            type: Object,
            required: true,
        },
    },
    setup(props, { emit }) {
        return {
            config: {
                toolbar: false,
                // sidebar: false;
            },
            closeModal: () => emit("closeModal"),
        }
    }
})
</script>

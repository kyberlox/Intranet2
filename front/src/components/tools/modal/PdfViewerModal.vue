<template>
    <div class="modal modal--fullscreen fade show"
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
                    <vue-pdf-app style="height: 100%;"
                                 theme="dark"
                                 :pdf='activeGazete.indirect_data.pdf'
                                 :config="config"
                                 :page-scale="'actual-size'"
                                 :page-number="1" />
                </div>
                <div class="modal-footer">
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import VuePdfApp from "vue3-pdf-app";
import "vue3-pdf-app/dist/icons/main.css";

export default defineComponent({
    props: {
        activeGazete: {
            type: Object,
            required: true,
        },
    },
    components: {
        VuePdfApp
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
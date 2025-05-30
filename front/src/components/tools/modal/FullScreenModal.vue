<template>
    <div class="modal modal--fullscreen fade show"
         style="display: block;">
        <div class="modal-dialog modal-fullscreen">
            <div class="modal-content modal-content--fullscreen">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">{{ activeGazete.title ? 'Корпоративная газета ' + activeGazete.title :
                        '' }}</h1>
                    <button @click="closeModal"
                            type="button"
                            class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <vue-pdf-app v-if="pageType == 'pdf'"
                                 style="height: 100%;"
                                 theme="light"
                                 :pdf='activeGazete.pdfUrl'
                                 :config="config"
                                 :page-scale="'actual-size'"
                                 :page-number="1"></vue-pdf-app>
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
        pageType: {
            type: String,
            default: "pdf"
        }
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
<template>
    <div class="page__title mt20">Корпоративная газета ЭМК</div>
    <div class="row gazettes-list">
        <div class="col-sm-3"
             @click="openModal(gazette)"
             v-for="gazette in gazettes"
             :key="gazette.id">
            <figure>
                <div class="gazette-image img-fluid img-thumbnail"
                     :style="{ 'background-image': `url(${gazette.src})` }"></div>
            </figure>
            <div>{{ gazette.title }}</div>
        </div>
    </div>
    <Transition name="modal">
        <PdfViewerModal v-if="modalActive"
                        :activeGazete="activeGazete"
                        @closeModal="modalActive = false" />
    </Transition>
</template>
<script lang="ts">
import { ref, defineComponent } from "vue";
import { gazettes } from "@/assets/static/gazettes";
import PdfViewerModal from "@/components/tools/modal/PdfViewerModal.vue";
import type { IGazette } from "@/interfaces/IGazettes";

export default defineComponent({
    components: {
        PdfViewerModal
    },
    setup() {
        const modalActive = ref(false);
        const activeGazete = ref();
        const openModal = (gazette: IGazette) => {
            modalActive.value = true;
            activeGazete.value = gazette;
        }
        return {
            gazettes,
            modalActive,
            openModal,
            activeGazete
        };
    },
});
</script>
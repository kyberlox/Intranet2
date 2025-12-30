<template>
<div class="page__title mt20">Корпоративная газета ЭМК</div>
<div class="row gazettes-list">
    <div class="col-sm-3"
         @click="openModal(gazette)"
         v-for="gazette in gazettes"
         :key="gazette.id">
        <figure>
            <div class="gazette-image img-fluid img-thumbnail"
                 :style="{ 'background-image': `url(${gazette.indirect_data.photo_file_url})` }"></div>
        </figure>
        <div>{{ gazette.name }}</div>
    </div>
</div>
<Transition name="modal">
    <PdfViewerModal v-if="modalActive"
                    :activeGazete="activeGazete"
                    @closeModal="modalActive = false" />
</Transition>
</template>


<script lang="ts">
import { ref, defineComponent, onMounted, type Ref } from "vue";
// import { gazettes } from "@/assets/static/gazettes";
// import type { IGazette } from "@/interfaces/IGazettes";
import PdfViewerModal from "@/components/tools/modal/PdfViewerModal.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import type { IBXFileType } from "@/interfaces/IEntities";

interface IGazette {
    id: number,
    name: string,
    indirect_data: {
        pdf: string,
        year: string,
        photo_file_url: string,
        documentation: IBXFileType[]
    },
}

export default defineComponent({
    components: {
        PdfViewerModal
    },
    setup() {
        const modalActive = ref(false);
        const gazettes: Ref<IGazette[]> = ref([]);
        const activeGazete = ref();

        const openModal = (gazette: IGazette) => {
            modalActive.value = true;
            activeGazete.value = gazette;
        }

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['газетта']}`)
                .then((data) => {
                    gazettes.value = data;
                })
        })

        return {
            gazettes,
            modalActive,
            openModal,
            activeGazete
        };
    },
});
</script>
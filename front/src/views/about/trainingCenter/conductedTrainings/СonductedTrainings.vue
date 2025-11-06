<template>
    <div class="conducted-training__page mt20">
        <div class="page__title">Проведённые тренинги</div>
        <TrainingTable :tableElements="trainings"
                       :page="'conductedTrainings'"
                       @openModal="(item: IConductedTrainings) => handleModal('open', item)" />

        <SlotModal v-if="modalIsVisible"
                   @close="handleModal('close', null)">
            <FeedBackModalInner :trainingInModal="trainingInModal" />
        </SlotModal>
    </div>
</template>

<script lang="ts">
import TrainingTable from "../components/TrainingTable.vue";
import { defineComponent, onMounted, ref, type Ref } from "vue";
import Api from "@/utils/Api";
import FeedBackModalInner from "@/views/about/trainingCenter/conductedTrainings/FeedBackModalInner.vue";
import { sectionTips } from "@/assets/static/sectionTips";
import type { IConductedTrainings } from "@/interfaces/IEntities";
import SlotModal from "@/components/tools/modal/SlotModal.vue";

export default defineComponent({
    components: {
        TrainingTable,
        SlotModal,
        FeedBackModalInner
    },
    setup() {
        const trainings: Ref<IConductedTrainings[]> = ref([]);
        const trainingInModal: Ref<IConductedTrainings> = ref({} as IConductedTrainings);
        const modalIsVisible = ref(false);

        onMounted(() => {
            Api.get(`/article/find_by/${sectionTips['проведенныеТренинги']}`)
                .then((data) => {
                    trainings.value = data;
                })
        })

        const handleModal = (type: string, item: IConductedTrainings | null) => {
            if (type == 'open' && item) {
                trainingInModal.value = item;
                modalIsVisible.value = true;
            }
            else {
                modalIsVisible.value = false
            }
        }
        return {
            trainings,
            trainingInModal,
            modalIsVisible,
            handleModal
        };
    },
});
</script>

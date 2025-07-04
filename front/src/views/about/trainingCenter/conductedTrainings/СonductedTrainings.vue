<template>
    <div class="conducted-training__page mt20">
        <div class="page__title">Проведённые тренинги</div>
        <TrainingTable :tableElements="trainings"
                       :page="'conductedTrainings'"
                       @openModal="(x) => handleModal('open', x)" />
        <FeedBackModal v-if="modalIsVisible == true"
                       @closeModal="handleModal('close', '')"
                       :trainingInModal="trainingInModal" />
    </div>
</template>

<script lang="ts">
import TrainingTable from "../components/TrainingTable.vue";
import { defineComponent, onMounted, ref, type Ref } from "vue";
import Api from "@/utils/Api";
import FeedBackModal from "@/views/about/trainingCenter/conductedTrainings/FeedBackModal.vue"
import { sectionTips } from "@/assets/static/sectionTips";
import type { IConductedTrainings } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        TrainingTable,
        FeedBackModal
    },
    setup() {
        const trainings: Ref<IConductedTrainings[]> = ref([]);
        const trainingInModal = ref();
        const modalIsVisible = ref(false);

        onMounted(() => {
            Api.get(`/article/find_by/${sectionTips['проведенныеТренинги']}`)
                .then((data) => {
                    trainings.value = data;
                })
        })

        const handleModal = (type, item) => {
            console.log('tip', type);
            console.log(item);


            if (type == 'open') {
                trainingInModal.value = item;
                modalIsVisible.value = true;
            }
            else {
                console.log('zakr')
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

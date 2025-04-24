<template>
    <div class="staff__item-wrapper col-sm-2"
         v-for="item in workers"
         :key="item.ID">

        <div class="staff__item"
             @click="handleClick(item)">
            <div class="img-fluid staff__item-img"
                 :style="{ backgroundImage: 'url(https://placehold.co/240x330)' }">
            </div>
            <div class="staff__item-name">
                {{ item.NAME }}
            </div>
            <div class="staff__item-position">{{ item.PROPERTY_1037 }}</div>
            <div class="staff__item-organisation">{{ item.PROPERTY_1069 }}</div>
            <div class="staff__item-organisation">{{ item.PROPERTY_1039 }}</div>
        </div>
        <ResultModal :worker="workerInModal"
                     :isOpen="isOpen"
                     @closeModal="closeModal" />
    </div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import type { IWorkersResults } from '@/interfaces/IWorkersOfTheYear';
import ResultModal from "./ResultModal.vue";

export default defineComponent({
    props: {
        workers: {
            type: Array<IWorkersResults>,
            required: true
        }
    },
    components: {
        ResultModal
    },
    setup(props) {
        const workerInModal = ref<IWorkersResults>();
        const isOpen = ref(false);
        const handleClick = (item: IWorkersResults) => {
            workerInModal.value = item;
            isOpen.value = true;
        }
        const closeModal = () => {
            isOpen.value = false;
        }
        return {
            handleClick,
            closeModal,
            workerInModal,
            isOpen
        }
    }
})
</script>
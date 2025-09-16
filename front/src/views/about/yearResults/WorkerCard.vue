<template>
<div class="staff__item-wrapper ">
    <div class="staff__item col-sm-2"
         v-for="item in workers"
         :key="item.id"
         @click="handleClick(item)">
        <div class="staff__item__inner"
             v-if="item.indirect_data">
            <div class="img-fluid staff__item-img"
                 v-lazy-load="formatSpacesInImg(item.indirect_data.photo_file_url)">
            </div>
            <div class="staff__item-name">
                {{ item.name }}
            </div>
            <div class="staff__item-position">
                {{ item.indirect_data.department }}
            </div>
            <div class="staff__item-organisation">
                {{ item.indirect_data.position }}
            </div>
            <div v-if="item.indirect_data.location"
                 class="staff__item-organisation">
                {{ item.indirect_data.location }}
            </div>
        </div>
    </div>
    <ResultModal :worker="workerInModal"
                 :isOpen="isOpen"
                 @closeModal="closeModal" />
</div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import type { IWorkerOfTheYear } from '@/interfaces/IEntities';
import ResultModal from "./ResultModal.vue";

export default defineComponent({
    props: {
        workers: {
            type: Array<IWorkerOfTheYear>,
            required: true
        }
    },
    components: {
        ResultModal
    },
    setup() {
        const workerInModal = ref<IWorkerOfTheYear>();
        const isOpen = ref(false);
        const handleClick = (item: IWorkerOfTheYear) => {
            workerInModal.value = item;
            isOpen.value = true;
        }
        const closeModal = () => {
            isOpen.value = false;
        }

        const formatSpacesInImg = (imgPath: string) => {
            const basePath = imgPath.split('user');
            const newPath = `${basePath[0]}user${encodeURIComponent(basePath[1])}`;
            return newPath;
        }
        return {
            handleClick,
            closeModal,
            workerInModal,
            isOpen,
            formatSpacesInImg
        }
    }
})
</script>
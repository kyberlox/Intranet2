<template>
    <Transition name="modal">
        <div v-if="isOpen && worker"
             class="modal__overlay"
             @click="closeModal">
            <div class="modal__wrapper">
                <div class="modal__header">
                    <h5 class="modal__title">{{ worker.name }}</h5>
                    <button class="modal__close-btn"
                            @click="closeModal"></button>
                </div>
                <div class="modal__body">
                    <div class="modal__grid">
                        <div class="modal__left">
                            <img class="modal__image"
                                 :src="'/src/assets/imgs/about/yearResults/gazinskii.png'" />
                            <span class="modal__name">{{ worker.name }}</span>
                            <div class="modal__position">{{ worker.position }}</div>
                            <div class="modal__department">{{ worker.department }}</div>
                        </div>
                        <div class="modal__right">
                            <div class="modal__description"
                                 v-html="worker.description"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>
<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
    props: {
        isOpen: {
            type: Boolean,
            default: false,
        },
        worker: {
            type: Object,
        },
    },
    setup(props, { emit }) {
        console.log(props)
        const item = {
            name: 1,
            position: 1,
            department: 1,
            description: 1,
        };
        const closeModal = () => {
            emit("closeModal");
        };
        return { item, closeModal };
    },
});
</script>

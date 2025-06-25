<template>
    <Transition name="modal">
        <div v-if="isOpen && worker"
             class="modal__overlay"
             @click="closeModal">
            <div class="modal__wrapper modal__wrapper--fixedHeight">
                <div class="modal__header">
                    <h5 class="modal__title">{{ worker.name }}</h5>
                    <button class="modal__close-btn"
                            @click="closeModal"></button>
                </div>
                <div class="modal__body">
                    <div class="modal__grid modal__grid--fixedHeight">
                        <div class="modal__left">
                            <div class="modal__image img-fluid staff__item-img modal__image--staff"
                                 v-lazy-load="worker.indirect_data.photo_file_url"
                                 alt="фото сотрудника">
                            </div>
                            <span class="modal__name">{{ worker.name }}</span>
                            <div class="modal__position">{{ worker.indirect_data.position }}</div>
                            <div class="modal__department">{{ worker.indirect_data.department }}</div>
                        </div>
                        <div class="modal__right">
                            <div class="modal__description"
                                 v-html="parseMarkdown(worker.content_text)"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>
<script lang="ts">
import { parseMarkdown } from "@/utils/useMarkdown";
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

        const closeModal = () => {
            emit("closeModal");
        };
        return {
            closeModal,
            parseMarkdown
        };
    },
});
</script>

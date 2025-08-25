<template>
    <div class="modal__overlay modal__overlay--zoom">
        <div @click="$emit('closeModal')"
             class="modal__overlay__close-button">
            <CloseIcon />
        </div>
        <div class="modal__wrapper modal__wrapper--zoom">
            <div class="modal__body modal__body--zoom">

                <div class="training-feedback__wrapper">
                    <div class="training-feedback"
                         v-for="(review, index) in trainingInModal?.indirect_data?.reviews"
                         :key="index">
                        <h1 v-if="review.reviewer">{{ review.reviewer }}</h1>
                        <h1 v-if="review.text"
                            v-html="review.text"></h1>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import type { IConductedTrainings } from '@/interfaces/IEntities';
import CloseIcon from '@/assets/icons/layout/CloseIcon.svg?component'

export default defineComponent({
    props: {
        trainingInModal: {
            type: Object as PropType<IConductedTrainings>
        }
    },
    components: {
        CloseIcon
    },
    setup() {
        return {
        }
    }
})
</script>
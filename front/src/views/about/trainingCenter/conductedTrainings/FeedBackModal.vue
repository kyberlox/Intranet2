<template>
    <div class="modal__overlay modal__overlay--zoom">
        <div @click="$emit('closeModal')"
             class="modal__overlay__close-button">
            <svg xmlns="http://www.w3.org/2000/svg"
                 width="30px"
                 height="30px"
                 viewBox="0 0 100 100"
                 version="1.1">

                <path style="fill:currentColor;stroke:#222222;stroke-width:4;"
                      d="M 20,4 3,21 33,50 3,80 20,97 49,67 79,97 95,80 65,50 95,20 80,4 50,34 z" />
            </svg>
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
import { propertyCheck } from '@/utils/propertyCheck';

export default defineComponent({
    props: {
        trainingInModal: {
            type: Object as PropType<IConductedTrainings>
        }
    },
    setup() {

        return {
            propertyCheck
        }
    }
})
</script>
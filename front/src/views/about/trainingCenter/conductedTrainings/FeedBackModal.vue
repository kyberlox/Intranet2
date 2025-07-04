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
                         v-for="(review, index) in trainingInModal.indirect_data.reviews"
                         :key="index">
                        <h1>{{ review.reviewer }}</h1>
                        <h1 v-html="review.text"></h1>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    props: {
        trainingInModal: {
            type: Object
        }
    },
    setup(props, { emit }) {
        console.log(props)

        return {

        }
    }
})
</script>
<style lang="scss">
.training-feedback__wrapper {
    background-color: #fff;
    padding: 24px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    max-height: 800px;
    overflow: auto;
}

.training-feedback {
    margin-bottom: 24px;
    padding: 16px;
    background-color: #f8f8f8;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.training-feedback h1 {
    margin: 0 0 12px 0;
    font-size: 18px;
    font-weight: 600;
    color: #333;
}

.training-feedback h1+h1 {
    margin: 0;
    font-size: 16px;
    font-weight: 400;
    color: #666;
    line-height: 1.7;
}

@media (max-width: 768px) {
    .training-feedback__wrapper {
        padding: 16px;
    }

    .training-feedback {
        padding: 12px;
    }

    .training-feedback h1 {
        font-size: 16px;
    }

    .training-feedback h1+h1 {
        font-size: 14px;
    }
}
</style>
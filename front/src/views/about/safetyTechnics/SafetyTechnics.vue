<template>
    <div class="page__title mt20">Техника безопасности</div>
    <div class="d-flex flex-column">
        <div class="section__image__list__section order-1 order-md-2">
            <div class="section__image__list__items row">
                <SafetyTechnicsSlide v-for="slide in safetyTechnicsSlides"
                                     :key="slide.id"
                                     :slide="slide" />

                <div class="col-12 col-xl-12 col-xxl-3">
                    <div class="news__detail__discr safety__section__discr"
                         v-html="sideInfoBlock"></div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import SafetyTechnicsSlide from "./components/SafetyTechnicsSlide.vue";
import { defineComponent } from "vue";
import { safetyTechnicsSlides, sideInfoBlock } from "@/assets/staticJsons/safetyTechnics";
export default defineComponent({
    components: {
        SafetyTechnicsSlide,
    },
    setup() {

        return {
            safetyTechnicsSlides,
            sideInfoBlock,
        };
    },
});
</script>

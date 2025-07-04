<template>
    <div class="page__title mt20">COVID-19</div>
    <div class="d-flex flex-column">
        <div class="section__image__list__section order-1 order-md-2">
            <div class="section__image__list__items row">
                <VerticalSlider v-if="safetyTechnicsCovidInner.content"
                                :slides="safetyTechnicsCovidInner.content"
                                :modifiers="['needLogo']" />

                <div class="col-12 col-xl-12 col-xxl-3"
                     v-html="safetyTechnicsCovidInner.sideInfo">
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { safetyTechnicsCovidInner } from "@/assets/static/safetyTechnics";
import VerticalSlider from "@/components/tools/swiper/VerticalSlider.vue";
export default defineComponent({
    components: {
        VerticalSlider
    },
    setup() {
        return {
            safetyTechnicsCovidInner,
        };
    },
});
</script>
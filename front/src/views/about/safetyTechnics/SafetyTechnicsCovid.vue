<template>
    <div class="page__title mt20">COVID-19</div>
    <div class="d-flex flex-column">
        <div class="section__image__list__section order-1 order-md-2">
            <div class="section__image__list__items row">
                <VerticalSlider v-for="slide in safetyTechnicsCovidInner.content"
                                     :key="slide.id"
                                     :slide="slide"
                                     :place="'inner'" />

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
import 
export default defineComponent({

    setup() {
        return {
            safetyTechnicsCovidInner,
        };
    },
});
</script>
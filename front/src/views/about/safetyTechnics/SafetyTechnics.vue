<template>
    <div class="page__title mt20">Техника безопасности</div>
    <div class="d-flex flex-column">
        <div class="section__image__list__section order-1 order-md-2">
            <div class="section__image__list__items row">
                <VerticalSlider v-if="safetyTechnics.content"
                                :page="'safetyTechnics'"
                                :slides="safetyTechnics.content" />
                <div class="col-12 col-xl-12 col-xxl-3">
                    <div class="news__detail__discr safety__section__discr"
                         v-html="safetyTechnics.sideInfo">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { safetyTechnics } from "@/assets/static/safetyTechnics";
import VerticalSlider from "@/components/tools/swiper/VerticalSlider.vue";
export default defineComponent({
    components: {
        VerticalSlider
    },
    setup() {
        return {
            safetyTechnics,
        };
    },
});
</script>

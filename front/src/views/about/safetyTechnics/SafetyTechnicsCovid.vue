<template>
    <div class="page__title mt20">COVID-19</div>
    <div class="d-flex flex-column">
        <div class="section__image__list__section order-1 order-md-2">
            <div class="section__image__list__items row">
                <div class="safety__section col-xxl-9">
                    <div v-for="(item, index) in safetyTechnicsCovidInner.content"
                         :key="'safe' + index"
                         class="safetyTechnics__card">
                        <VerticalCard :card="item"
                                      :modifiers="['needLogo']" />
                    </div>
                </div>
                <div class="col-12 col-xl-12 col-xxl-3">
                    <div class="news__detail__discr safety__section__discr"
                         v-html="safetyTechnicsCovidInner.sideInfo">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { safetyTechnicsCovidInner } from "@/assets/static/safetyTechnics";
import VerticalCard from "../../../components/tools/common/VerticalCard.vue";

export default defineComponent({
    components: {
        VerticalCard
    },
    setup() {
        return {
            safetyTechnicsCovidInner,
        };
    },
});
</script>
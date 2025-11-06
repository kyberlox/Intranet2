<template>
<div class="mt20">
    <div class="page__title">Пожарная безопасность и эвакуация из офисного здания</div>
    <PostInner :previewElement="safetyTechnicsFireInner.content" />
    <div class="safety__section__evacuation">
        <div class="safety__section__evacuation__swiper-wrapper">
            <SwiperBlank :activeIndexInModal="activeIndexInModal"
                         :type="'second'"
                         :images="safetyTechnicsFireInner?.evacuationContent?.images" />
        </div>
        <div class="safety__section__evacuation__floors-list">
            <h4>План эвакуации по этажам</h4>
            <div class="safety__section__evacuation__floor"
                 @click="activeIndexInModal = index"
                 v-for="(i, index) in [1, 3, 6, 7, 8, 9, 10, 11, 12]"
                 :key="index">
                {{ `Этаж ${i}` }}
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import PostInner from "@/components/tools/common/PostInner.vue";
import SwiperBlank from "@/components/tools/swiper/SwiperBlank.vue";
import { defineComponent, ref } from "vue";
import { safetyTechnicsFireInner } from "@/assets/static/safetyTechnics";
export default defineComponent({
    components: {
        PostInner,
        SwiperBlank
    },
    setup() {
        const activeIndexInModal = ref();
        return {
            activeIndexInModal,
            safetyTechnicsFireInner
        };
    },
});
</script>
<template>
    <h2 class="page__title mt20">
        Новые сотрудники
    </h2>
    <div class="row mb-5 mt20">
        <div class="newWorkers__page-swiper__wrapper pos-rel"
             v-if="newWorkers.length">
            <swiper class="newWorkers__page__swiper"
                    v-bind="sliderConfig"
                    @swiper="swiperOn">
                <swiper-slide v-for="(slide, index) in newWorkers"
                              :key="'vertSlide' + index">
                    <VerticalSliderSlide :slide="slide" />
                </swiper-slide>
            </swiper>

            <SwiperButtons :isBeginning="isBeginning"
                           :isEnd="isEnd"
                           @slideNext="slideNext"
                           @slidePrev="slidePrev" />
        </div>
    </div>
</template>

<script lang="ts">
import { sectionTips } from '@/assets/static/sectionTips';
import Api from '@/utils/Api';
import { defineComponent, onMounted, ref } from 'vue';
import { useSwiperconf } from '@/composables/useSwiperConf';
import VerticalSliderSlide from '@/components/tools/swiper/VerticalSliderSlideUsers.vue';
import SwiperButtons from '@/components/tools/swiper/SwiperButtons.vue';
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/navigation";

export default defineComponent({
    name: "newWorkers",
    components: {
        SwiperButtons,
        VerticalSliderSlide,
        Swiper,
        SwiperSlide
    },
    setup() {
        const newWorkers = ref([]);
        const swiperConf = useSwiperconf('vertical');

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['НовыеСотрудники']}`)
                .then((data) => newWorkers.value = data)
        })

        return {
            newWorkers,
            swiperConf,
            isEnd: swiperConf.isEnd,
            swiperOn: swiperConf.swiperOn,
            slideNext: swiperConf.slideNext,
            slidePrev: swiperConf.slidePrev,
            sliderConfig: swiperConf.sliderConfig,
            swiperInstance: swiperConf.swiperInstance,
            isBeginning: swiperConf.isBeginning,
        }
    }
})
</script>

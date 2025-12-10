<template>
<div class="page__title mt20">Дни рождения</div>
<div class="row">
    <div class="col-12">
        <ul class="birthday__chain-nav">
            <li v-for="nav in fastDayNavigation"
                :key="'picker' + nav.id"
                class="birthday__chain-nav__item"
                :class="{ 'birthday__chain-nav__item--active': searchValue == nav.value }"
                @click="pickDate(nav.value, true)">{{ nav.text }}</li>
        </ul>
    </div>
</div>
<div class="birthday__date-picker-wrapper mt20">
    <div class="col-12 col-md-2 mb-3">
        <DatePicker @pickDate="(date: string) => pickDate(date)"
                    :calendarType="'dayAndMonth'"
                    :nullifyDateInput="nullifyDateInput" />
    </div>
</div>
<div class="birthday__workers-grid">
    <div class="birthday__page-content">
        <div class="birthday__page__swiper__wrapper"
             v-if="slidesForBirthday.length && !isLoading">
            <swiper class="birthday__page__swiper"
                    v-bind="sliderConfig"
                    @swiper="swiperOn">
                <swiper-slide v-for="(slide, index) in slidesForBirthday"
                              :key="'vertSlide' + index">
                    <VerticalSliderSlide :needCakeIcon="true"
                                         :slide="slide" />
                </swiper-slide>
            </swiper>
            <SwiperButtons :isBeginning="isBeginning"
                           :isEnd="isEnd"
                           @slideNext="slideNext"
                           @slidePrev="slidePrev" />
        </div>
        <div v-else
             class="birthday__page__swiper__wrapper">
            <Loader class="contest__page__loader" />
        </div>
        <div class="birthday__static__greetings">
            <img @click="openModal([birthdayPageImg])"
                 :src=birthdayPageImg
                 alt="поздравление" />
        </div>
    </div>
</div>
<Transition name="modal">
    <ZoomModal v-if="!hiddenModal"
               :image="imageInModal"
               @close="hiddenModal = true; imageInModal = '';" />
</Transition>
</template>

<script lang="ts">
import { ref, watch, nextTick, defineComponent } from "vue";
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import "@vuepic/vue-datepicker/dist/main.css";
import DatePicker from "@/components/tools/common/DatePicker.vue";
import Api from "@/utils/Api";
import { useSwiperconf } from "@/composables/useSwiperConf";
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
import "swiper/css/navigation";
import VerticalSliderSlide from '@/components/tools/swiper/VerticalSliderSlideUsers.vue';
import SwiperButtons from '@/components/tools/swiper/SwiperButtons.vue';
import birthdayPageImg from "@/assets/imgs/plugs/birthdayPlug.png";
import Loader from "@/components/layout/Loader.vue";

export default defineComponent({
    components: {
        DatePicker,
        Swiper,
        SwiperSlide,
        VerticalSliderSlide,
        SwiperButtons,
        ZoomModal,
        Loader
    },
    setup() {
        const isLoading = ref(false);
        const today = new Date();
        const yesterday = new Date(today);
        const tomorrow = new Date(today);

        const formatDate = (date: Date) => {
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0');
            return `${day}.${month}`;
        };

        const slidesForBirthday = ref([]);
        const searchValue = ref(formatDate(today));
        const imageInModal = ref();
        const hiddenModal = ref(true);

        const openModal = (url: [string]) => {
            imageInModal.value = url;
            hiddenModal.value = false;
        };

        const pickDate = (target: string | Date, needNulify: boolean = false) => {
            searchValue.value = String(target).length > 5 ? formatDate(target as Date) : String(target);
            if (needNulify) {
                nullifyDateInput.value = true;
            }
            nextTick(() => {
                nullifyDateInput.value = false;
            });
        }

        yesterday.setDate(today.getDate() - 1);
        tomorrow.setDate(today.getDate() + 1);

        const fastDayNavigation = [
            {
                id: 1,
                text: "Дни Рождения вчера",
                value: formatDate(yesterday),
            },
            {
                id: 2,
                text: "Сегодня День Рождения отмечают",
                value: formatDate(today),
            },
            {
                id: 3,
                text: "Дни Рождения завтра",
                value: formatDate(tomorrow),
            },
        ];

        // onMounted(() => {
        //     Api.get(`article/find_by/${sectionTips['ДниРождения']}`)
        //         .then((data) => slidesForBirthday.value = data)
        // })

        watch((searchValue), (newVal) => {
            if (!newVal) return;
            isLoading.value = true;
            Api.get(`users/get_birthday_celebrants/${String(searchValue.value)}`)
                .then((data) => slidesForBirthday.value = data)
                .finally(() => isLoading.value = false)
        }, { immediate: true, deep: true })

        const dateFromDatepicker = ref();
        const nullifyDateInput = ref(false);

        const swiperConf = useSwiperconf('vertical');

        return {
            slidesForBirthday,
            imageInModal,
            hiddenModal,
            fastDayNavigation,
            searchValue,
            dateFromDatepicker,
            isLoading,
            nullifyDateInput,
            openModal,
            pickDate,
            isEnd: swiperConf.isEnd,
            sliderConfig: swiperConf.sliderConfig,
            swiperInstance: swiperConf.swiperInstance,
            isBeginning: swiperConf.isBeginning,
            birthdayPageImg,
            swiperOn: swiperConf.swiperOn,
            slideNext: swiperConf.slideNext,
            slidePrev: swiperConf.slidePrev,
        };
    },
});
</script>
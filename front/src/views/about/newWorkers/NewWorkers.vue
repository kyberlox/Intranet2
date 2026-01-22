<template>
<div class="page__title mt20">Новые сотрудники</div>
<div class="birthday__workers-grid"
     v-if="slidesForBirthday.length && !isLoading">
    <div v-for="(slide, index) in slidesForBirthday"
         :key="'vertSlide' + index">
        <VerticalSliderSlide :needCakeIcon="true"
                             :slide="slide" />
    </div>
</div>
<div v-else-if="isLoading"
     class="contest__page__loader">
    <Loader />
</div>
<ContentPlug :plugText="noWorkers"
             :plugImg="noWorkersImage"
             v-else />
</template>

<script lang="ts">
import { ref, defineComponent, onMounted } from "vue";
import "@vuepic/vue-datepicker/dist/main.css";
import Api from "@/utils/Api";
import VerticalSliderSlide from '@/components/tools/swiper/VerticalSliderSlideUsers.vue';
import birthdayPageImg from "@/assets/imgs/plugs/birthdayPlug.png";
import Loader from "@/components/layout/Loader.vue";
import { noWorkers } from "@/assets/static/contentPlugs";
import ContentPlug from "@/components/layout/ContentPlug.vue";
import noWorkersImage from "@/assets/imgs/plugs/contentPlugWorkers.jpg";
import { sectionTips } from "@/assets/static/sectionTips";

export default defineComponent({
    components: {
        VerticalSliderSlide,
        Loader,
        ContentPlug
    },
    setup() {
        const isLoading = ref(false);

        const slidesForBirthday = ref([]);
        const imageInModal = ref();
        const hiddenModal = ref(true);

        const openModal = (url: [string]) => {
            imageInModal.value = url;
            hiddenModal.value = false;
        };

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['НовыеСотрудники']}`)
                .then((data) => slidesForBirthday.value = data)
        })


        const dateFromDatepicker = ref();
        const nullifyDateInput = ref(false);


        return {
            slidesForBirthday,
            imageInModal,
            hiddenModal,
            dateFromDatepicker,
            isLoading,
            nullifyDateInput,
            openModal,
            birthdayPageImg,
            noWorkers,
            noWorkersImage
        };
    },
});
</script>
<template>
<div class="page__title mt20">Новые сотрудники</div>
<div v-if="isLoading"
     class="contest__page__loader">
    <Loader />
</div>

<div v-else-if="slidesForBirthday.length && !isLoading"
     class="birthday__workers-grid">
    <div v-for="(slide, index) in slidesForBirthday"
         :key="'vertSlide' + index">
        <UserSlide :needCakeIcon="false"
                   :slide="slide" />
    </div>
</div>

<ContentPlug v-else
             :plugText="noWorkers"
             :plugImg="noWorkersImage" />
</template>

<script lang="ts">
import { ref, defineComponent, onMounted } from "vue";
import "@vuepic/vue-datepicker/dist/main.css";
import Api from "@/utils/Api";
import UserSlide from "@/components/layout/UserSlide.vue";
import birthdayPageImg from "@/assets/imgs/plugs/birthdayPlug.png";
import Loader from "@/components/layout/Loader.vue";
import { noWorkers } from "@/assets/static/contentPlugs";
import ContentPlug from "@/components/layout/ContentPlug.vue";
import noWorkersImage from "@/assets/imgs/plugs/contentPlugWorkers.jpg";
import { sectionTips } from "@/assets/static/sectionTips";

export default defineComponent({
    components: {
        UserSlide,
        Loader,
        ContentPlug
    },
    setup() {
        const isLoading = ref(true);
        const dateFromDatepicker = ref();
        const nullifyDateInput = ref(false);
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
                .finally(() => isLoading.value = false)
        })

        return {
            slidesForBirthday,
            imageInModal,
            hiddenModal,
            dateFromDatepicker,
            isLoading,
            nullifyDateInput,
            birthdayPageImg,
            noWorkers,
            noWorkersImage,
            openModal,
        };
    },
});
</script>
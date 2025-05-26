<template>
    <div class="page__title mt20">Дни рождения</div>
    <div class="row">
        <div class="col-12">
            <ul class="birthday__chain-nav">
                <li v-for="nav in fastDayNavigation"
                    :key="'picker' + nav.id"
                    class="birthday__chain-nav__item"
                    :class="{ 'birthday__chain-nav__item--active': searchValue == nav.value }"
                    @click="pickDate(nav.value)">{{ nav.text }}</li>
            </ul>
        </div>
    </div>
    <div class="birthday__date-picker-wrapper mt20">
        <div class="col-12 col-md-2 mb-3">
            <DatePicker />
        </div>
    </div>
    <div class="birthday__workers-grid">
        <div class="row birthday__page-content">
            <div class="birthday__workers-slider">
                <VerticalSlider :page="'birthdays'"
                                :slides="slidesForBirthday" />
            </div>
            <div class="birthday__static__greetings">
                <img @click="openModal('https://portal.emk.ru/upload/disk/320/3205a776c4a005c8a856afc10f441488')"
                     src="https://portal.emk.ru/upload/disk/320/3205a776c4a005c8a856afc10f441488" />
            </div>
        </div>
    </div>
    <Transition name="modal">
        <ZoomModal v-if="!hiddenModal"
                   :image="imageInModal"
                   @close="
                    hiddenModal = true;
                imageInModal = '';
                " />
    </Transition>
</template>
<script lang="ts">
import { ref } from "vue";
import VerticalSlider from "@/components/tools/swiper/VerticalSlider.vue";
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import "@vuepic/vue-datepicker/dist/main.css";
import { slidesForBirthday, fastDayNavigation } from "@/assets/staticJsons/birthday";
import { defineComponent } from "vue";
import DatePicker from "@/components/DatePicker.vue";
export default defineComponent({
    components: {
        VerticalSlider,
        ZoomModal,
        DatePicker,
    },
    setup() {

        const imageInModal = ref();
        const hiddenModal = ref(true);

        const openModal = (url: string) => {
            imageInModal.value = url;
            hiddenModal.value = false;
        };


        return {
            slidesForBirthday,
            imageInModal,
            openModal,
            hiddenModal,
            fastDayNavigation,
        };
    },
});
</script>

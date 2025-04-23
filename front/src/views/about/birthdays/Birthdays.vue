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
            <VueDatePicker v-model="date"
                           locale="ru"
                           cancelText="Назад"
                           selectText="Ок"
                           :enable-time-picker="false"
                           disable-year-select
                           auto-apply
                           placeholder="Выберите дату"
                           :format="format" />
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
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { slidesForBirthday, fastDayNavigation } from "@/assets/staticJsons/birthday";
import { defineComponent } from "vue";
export default defineComponent({
    components: {
        VerticalSlider,
        ZoomModal,
        VueDatePicker,
    },
    setup() {
        const dateInput = ref();

        const searchValue = ref("20.01.2025");

        const pickDate = (date: string) => {
            searchValue.value = date;
        };

        const openDatePicker = () => {
            if (!dateInput.value) return;
            dateInput.value.showPicker();
        };

        const imageInModal = ref();
        const hiddenModal = ref(true);

        const openModal = (url: string) => {
            imageInModal.value = url;
            hiddenModal.value = false;
        };

        const date = ref(new Date());
        const format = (date: Date = new Date()) => {
            const day = date.getDate();
            const month = date.getMonth() + 1;

            return `${day > 9 ? day : "0" + day}.${month > 9 ? month : "0" + month}`;
        };

        return {
            dateInput,
            openDatePicker,
            slidesForBirthday,
            imageInModal,
            openModal,
            hiddenModal,
            fastDayNavigation,
            searchValue,
            pickDate,
            date,
            format,
        };
    },
});
</script>

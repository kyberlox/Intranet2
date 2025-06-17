<template>
    <div class="page__title mt20">Дни рождения</div>
    <div class="row">
        <div class="col-12">
            <ul class="birthday__chain-nav">
                <li v-for="nav in fastDayNavigation"
                    :key="'picker' + nav.id"
                    class="birthday__chain-nav__item"
                    :class="{ 'birthday__chain-nav__item--active': searchValue == nav.value }"
                    @click="pickDate(nav.value, true);">{{ nav.text }}</li>
            </ul>
        </div>
    </div>
    <div class="birthday__date-picker-wrapper mt20">
        <div class="col-12 col-md-2 mb-3">
            <DatePicker @chosenDate="(date) => pickDate(date)"
                        :calendarType="'dayAndMonth'"
                        :nullifyDateInput="nullifyDateInput" />
        </div>
    </div>
    <div class="birthday__workers-grid">
        <div class="row birthday__page-content">
            <div class="birthday__workers-slider">
                <VerticalSlider :page="'birthdays'"
                                :slides="slidesForBirthday" />
            </div>
            <div class="birthday__static__greetings">
                <img @click="openModal(['https://portal.emk.ru/upload/disk/320/3205a776c4a005c8a856afc10f441488'])"
                     src="https://portal.emk.ru/upload/disk/320/3205a776c4a005c8a856afc10f441488" />
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
import { onMounted, ref, watch, nextTick } from "vue";
import VerticalSlider from "@/components/tools/swiper/VerticalSlider.vue";
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import "@vuepic/vue-datepicker/dist/main.css";
// import { slidesForBirthday } from "@/assets/staticJsons/birthday";
import { defineComponent } from "vue";
import DatePicker from "@/components/DatePicker.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
export default defineComponent({
    components: {
        VerticalSlider,
        ZoomModal,
        DatePicker,
    },
    setup() {
        const slidesForBirthday = ref([]);
        const searchValue = ref();
        const imageInModal = ref();
        const hiddenModal = ref(true);

        const openModal = (url: [string]) => {
            imageInModal.value = url;
            hiddenModal.value = false;
        };

        const pickDate = (target: string, needNulify: boolean = false) => {
            searchValue.value = target;
            if (needNulify) {
                nullifyDateInput.value = true;
            }
            nextTick(() => {
                nullifyDateInput.value = false;
            });
        }

        const today = new Date();

        const yesterday = new Date(today);
        yesterday.setDate(today.getDate() - 1);

        const tomorrow = new Date(today);
        tomorrow.setDate(today.getDate() + 1);

        const formatDate = (date: Date) => {
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0');
            return `${day}.${month}`;
        };

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


        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['ДниРождения']}`)
                .then((data) => slidesForBirthday.value = data)
        })

        watch((searchValue), (newVal) => {
            if (!newVal) return;
            Api.get(`users/get_birthday_celebrants/${String(searchValue.value)}`)
                .then((data) => slidesForBirthday.value = data)
        }, { immediate: true, deep: true })

        const dateFromDatepicker = ref();

        const nullifyDateInput = ref(false);

        return {
            slidesForBirthday,
            imageInModal,
            openModal,
            hiddenModal,
            fastDayNavigation,
            searchValue,
            pickDate,
            dateFromDatepicker,
            nullifyDateInput
        };
    },
});
</script>

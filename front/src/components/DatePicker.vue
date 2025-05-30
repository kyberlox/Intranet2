<template>
    <VueDatePicker v-model="date"
                   locale="ru"
                   cancelText="Назад"
                   selectText="Ок"
                   :enable-time-picker="false"
                   disable-year-select
                   auto-apply
                   placeholder="Выберите дату"
                   :format="format" />
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
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

        const date = ref(new Date());
        const format = (date: Date = new Date()) => {
            const day = date.getDate();
            const month = date.getMonth() + 1;

            return `${day > 9 ? day : "0" + day}.${month > 9 ? month : "0" + month}`;
        };

        return {
            dateInput,
            openDatePicker,
            imageInModal,
            searchValue,
            pickDate,
            date,
            format,
        };
    }
})
</script>
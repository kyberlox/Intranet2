<template>
    <VueDatePicker v-model="dateInput"
                   locale="ru"
                   cancelText="Назад"
                   selectText="Ок"
                   :enable-time-picker="false"
                   disable-year-select
                   :six-weeks="true"
                   auto-apply
                   placeholder="Выберите дату"
                   :format="format"
                   @update:model-value="handleDate" />
</template>

<script lang="ts">
import { watch } from 'vue';
import { defineComponent, ref } from 'vue';

export default defineComponent({
    props: {
        calendarType: {
            type: String,
            default: 'dayAndMonth'
        },
        nullifyDateInput: {
            type: Boolean,
            default: false
        }
    },
    setup(props, { emit }) {
        const dateInput = ref();

        watch(() => props.nullifyDateInput, (newVal) => {
            if (newVal == true) {
                dateInput.value = null;
            }
        }, { deep: true, immediate: true })


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
            const year = date.getFullYear();
            if (props.calendarType == 'dayAndMonth') {
                return `${day > 9 ? day : "0" + day}.${month > 9 ? month : "0" + month}`;
            }
            else if (props.calendarType == 'monthAndYear') {
                return `${month > 9 ? month : "0" + month}.${year}`;
            }
        };

        const handleDate = (date: Date) => {
            if (!date) return;
            emit('chosenDate', format(date))
        }

        return {
            dateInput,
            openDatePicker,
            imageInModal,
            searchValue,
            pickDate,
            date,
            format,
            handleDate
        };
    }
})
</script>
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
                   :markers="markers"
                   @cleared="$emit('clearValue')"
                   @update:model-value="handleDate">
        <template #marker="{ marker }">
            <div class="calendar__custom-marker__wrapper"
                 @click="$emit('markerClick', marker)">
                <span class="calendar__custom-marker"
                      :style="{ backgroundColor: marker.color }">
                    <span>{{ marker.tooltip.name }}</span>
                </span>
            </div>
        </template>
    </VueDatePicker>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch } from 'vue';
import { type ICalendarMarker } from '@/components/layout/RightSidebarCalendar.vue';

export default defineComponent({
    name: 'DatePicker',
    props: {
        calendarType: {
            type: String,
            default: 'dayAndMonth'
        },
        nullifyDateInput: {
            type: Boolean,
            default: false
        },
        markers: {
            type: Array<ICalendarMarker>
        }
    },
    setup(props, { emit }) {
        const dateInput = ref();

        watch(() => props.nullifyDateInput, (newVal) => {
            if (newVal) {
                dateInput.value = null;
            }
        }, { deep: true, immediate: true })


        const searchValue = ref("");

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
            else if (props.calendarType == 'month') {
                return `${month > 9 ? month : "0" + month}`
            }
            else if (props.calendarType == 'full') {
                return `${day > 9 ? day : "0" + day}.${month > 9 ? month : "0" + month}.${year}`
            }
        };

        const handleDate = (date: Date) => {
            if (!date) return;
            emit('pickDate', date)
        }

        onMounted(() => {
            handleDate(dateInput.value);
            dateInput.value = new Date();
        })

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
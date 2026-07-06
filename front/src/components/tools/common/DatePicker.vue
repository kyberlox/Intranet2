<template>
<VueDatePicker v-model="dateInput"
               locale="ru"
               cancelText="Назад"
               selectText="Ок"
               :enable-time-picker="timePicker"
               disable-year-select
               :six-weeks="true"
               auto-apply
               placeholder="Выберите дату"
               :format="format"
               :dark="dark"
               :range=range
               :markers="markers"
               @cleared="$emit('clearValue')"
               @update:model-value="handleDate">
    <template #marker="{ marker }">
        <div class="calendar__custom-marker__wrapper"
             @click="$emit('markerClick', marker)">
            <span class="calendar__custom-marker"
                  :class="{ 'calendar__custom-marker--line': marker.type == 'line' }"
                  :style="{ backgroundColor: marker.color }">
                <span>{{ marker.tooltip.name }}</span>
            </span>
        </div>
    </template>
</VueDatePicker>
</template>

<script lang="ts">
import { defineComponent, ref, watch, computed, type PropType } from 'vue';
import { type ICalendarMarker } from '@/components/layout/sidebars/RightSidebarCalendar.vue';
import { useStyleModeStore } from '@/stores/styleMode';
import type { IAdminListItem } from '@/interfaces/IEntities';
import { dateConvert } from '@/utils/dateConvert';
import { calendarTypeFormat } from '@/utils/calendarTypeFormat';

export default defineComponent({
    name: 'DatePicker',
    props: {
        calendarType: {
            type: String as PropType<'dayAndMonth' | 'monthAndYear' | 'month' | 'fullNoYear' | 'full'>,
            default: 'dayAndMonth'
        },
        nullifyDateInput: {
            type: Boolean,
            default: false
        },
        markers: {
            type: Array<ICalendarMarker>
        },
        defaultData: {
            type: String
        },
        item: {
            type: Object as PropType<IAdminListItem>,
        },
        timePicker: {
            type: Boolean,
            default: false
        },
        range: {
            type: Boolean,
            default: false
        }
    },

    setup(props, { emit }) {
        const dateInput = ref();

        watch(() => props.nullifyDateInput, (newVal) => {
            if (newVal) {
                dateInput.value = '';
            }
        }, { deep: true, immediate: true })

        const handleDate = (date: Date) => {
            if (!date) return;
            emit('pickDate', date)
        }

        watch(() => props.defaultData, () => {
            if (props.defaultData) {
                dateInput.value = dateConvert(props.defaultData, 'toDateType');
                handleDate(dateInput.value);
            }
        }, { immediate: true })

        const openDatePicker = () => {
            if (!dateInput.value) return;
            dateInput.value.showPicker();
        };

        const imageInModal = ref();
        const date = ref(new Date());

        const format = (dateToFormat: Array<Date> | Date) => {
            console.log(dateToFormat);

            if (props.range && Array.isArray(dateToFormat)) {
                const from = calendarTypeFormat(props.calendarType, dateToFormat[0]);
                const to = calendarTypeFormat(props.calendarType, dateToFormat[1]);
                return from == to ? from : `${from}-${to}`
            }
            else
                return calendarTypeFormat(props.calendarType, dateToFormat as Date)
        }

        return {
            dateInput,
            imageInModal,
            date,
            openDatePicker,
            format,
            handleDate,
            dark: computed(() => useStyleModeStore().getDarkMode)
        };
    }
})
</script>

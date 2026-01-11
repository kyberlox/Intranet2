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
               :dark="dark"
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
import { defineComponent, onMounted, ref, watch, computed } from 'vue';
import { type ICalendarMarker } from '@/components/layout/RightSidebarCalendar.vue';
import { useStyleModeStore } from '@/stores/styleMode';

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
        },
        defaultData: {
            type: String
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
                const formatMonth = date.toLocaleString('ru', { 'month': 'long' })
                return formatMonth.charAt(0).toUpperCase() + formatMonth.slice(1);
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
            if (props.defaultData) {
                dateInput.value = new Date(props.defaultData);
            }
            else if (props.calendarType !== 'month') {
                dateInput.value = new Date();
            }
            handleDate(dateInput.value);
        })

        return {
            dateInput,
            imageInModal,
            searchValue,
            date,
            pickDate,
            openDatePicker,
            format,
            handleDate,
            dark: computed(() => useStyleModeStore().getDarkMode)
        };
    }
})
</script>
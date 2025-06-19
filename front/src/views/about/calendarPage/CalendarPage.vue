<template>
    <div class="page__title mt20">Календарь событий</div>
    <div class="calendar-container">
        <div class="calendar__meanings">
            <div class="calendar_meaning">Основные события<div class="square-mark"
                     style="background-color: #f36509"></div>
            </div>
            <div class="calendar_meaning">ОВК
                <div class="square-mark"
                     style="background-color: #00b38c">
                </div>
            </div>
        </div>

        <DatePicker v-model="date"
                    month-picker
                    :calendarType="'monthAndYear'" />
    </div>
    <div class="calendarYear mt20">
        <div class="calendarYear__item__wrapper"
             v-for="month in monthesInit"
             :key="'month' + month.value">
            <div class="calendarYear__item"
                 v-if="currentEvents.find((item) => item.month == month.value)">
                <div class="calendarYear__title "
                     :class="{ 'calendarYear__title--target': String(monthId) == month.value }"
                     :data-month-num="month.value"
                     ref=chosenMonth>{{ month.name }}</div>
                <div class="calendarYear__content">
                    <div class="calendarYear__event__wrapper"
                         v-for="event in currentEvents"
                         :key="event.id">
                        <div class="calendarYear__event"
                             v-if="event.month == month.value">
                            <span class="calendarYear__event__date">{{ event.date }}</span>
                            <span class="calendarYear__event__name">{{ event.name }}</span>
                            <div class="square-mark"></div>
                            <button v-if="checkButtonStatus(event)"
                                    class="calendarYear__event-btn calendarYear__event-btn_archive event-button">
                                {{ checkButtonStatus(event) }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, ref, watchEffect } from 'vue';
import { monthesInit, calendarPage } from '@/assets/staticJsons/calendar';
import type { ICalendarEntity } from '@/interfaces/ICalendar';
import DatePicker from '@/components/tools/common/DatePicker.vue';
export default defineComponent({
    components: {
        DatePicker
    },
    props: {
        monthId: {
            type: String
        }
    },
    setup(props) {
        const years = Object.keys(calendarPage);
        const currentYear = new Date().getFullYear();
        const currentEvents = calendarPage[currentYear];
        const checkButtonStatus = (event: ICalendarEntity) => {
            if (event.report) {
                return 'Как это было'
            }
            else if (event.past) {
                return 'Прошло'
            }
            else if (event.preview) {
                return 'Записаться'
            }
            else {
                return false
            }
        }
        const yearSelect = ref(new Date().getFullYear());

        const date = ref(new Date());

        const chosenMonth = ref();

        watchEffect(() => {
            if (chosenMonth.value) {
                chosenMonth.value.map((e: HTMLElement) => {
                    if (e.getAttribute('data-month-num') == props.monthId) {
                        setTimeout(() =>
                            e.scrollIntoView({ behavior: 'smooth', block: 'center' }), 10)
                    }
                })
            }
        })

        return {
            years,
            monthesInit,
            currentYear,
            yearSelect,
            currentEvents,
            checkButtonStatus,
            date,
            chosenMonth,
        };
    },
});
</script>

<style>
.calendarYear__title--target {
    background-color: rgba(0, 123, 255, 0.1);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #007bff;
    transition: all 0.3s ease;
}
</style>
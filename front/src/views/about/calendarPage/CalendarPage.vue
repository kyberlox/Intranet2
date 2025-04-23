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
        <div class="calendar__nav-group">
            <select class="calendarYear__nav-select month-select">
                <option selected
                        disabled>Укажите месяц</option>
                <option>Все месяцы</option>
                <option v-for="month in monthesInit"
                        :key="'month' + month.value">{{ month.name }}</option>
            </select>
            <select v-model="yearSelect"
                    class="calendarYear__nav-select year-select">
                <option selected
                        disabled>Укажите год</option>
                <option v-for="year in years"
                        :key="year + 'year'">{{ year }}</option>
            </select>
        </div>
    </div>
    <div class="calendarYear">
        <div class="calendarYear__item__wrapper"
             v-for="month in monthesInit"
             :key="'month' + month.value">
            <div class="calendarYear__item"
                 v-if="currentEvents.find((item) => item.month == month.value)">
                <div class="calendarYear__title">{{ month.name }}</div>
                <div class="calendarYear__content">
                    <div class="calendarYear__event__wrapper"
                         v-for="event in currentEvents"
                         :key="event.id">
                        <div class="calendarYear__event"
                             v-if="event.month == month.value">
                            <span class="calendarYear__event__date">{{ event.date }}</span>
                            <span class="calendarYear__event__name">{{ event.name }}</span>
                            <!-- <div style="width: 133px"></div> -->
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
import { defineComponent, ref } from 'vue';
import { monthesInit, calendarPage } from '@/assets/staticJsons/calendar';
import type { ICalendarEntity } from '@/interfaces/ICalendar';
export default defineComponent({
    setup() {
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
        return {
            years,
            monthesInit,
            currentYear,
            yearSelect,
            currentEvents,
            checkButtonStatus
        };
    },
});
</script>
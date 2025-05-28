<template>
    <div class="task__block"
         id="calendarPlace">
        <div class="calendar">
            <div class="calendar__title">{{ MonthName }} {{ currentYear }}</div>
            <div class="calendar__wrapper">
                <div class="calendar__inner">
                    <div class="calendar__item calendar__item_day"
                         v-for="item in weekDays"
                         :key="item">
                        {{ item }}
                    </div>
                    <div v-for="noDate in FirstDayOfMonth"
                         :key="'noDate' + noDate"
                         class="calendar__item calendar__item_empty"></div>
                    <div v-for="num in daysCountInCurrentMonth"
                         :key="'day' + num"
                         class="calendar__item"
                         :class="{ 'calendar__item_active': eventDates.includes(String(num)) }"
                         :data-day="num"
                         :data-date="formatNumLength(String(num)) + '.' + currentMonth + '.' + currentYear">
                        {{ num }}
                        <div v-if="eventDates.includes(String(num))"
                             class="tooltip-wrapper">
                            <div class="tooltipo">
                                <div v-for="(event, index) in calendarMiniDates[num]"
                                     :key="'event' + index">{{ event }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <RouterLink :to="{ name: 'calendar', params: { id: currentMonth } }"
                        class="calendar__button">Все события</RouterLink>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { calendarMiniDates } from '@/assets/staticJsons/calendar';

export default defineComponent({
    setup() {
        const now = new Date();

        const formatNumLength = (num: string) => {
            return Number(num) > 9 ? num : '0' + num
        }
        const weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

        const currentMonth = formatNumLength(String(now.getMonth() + 1));
        const currentYear = now.getFullYear();
        const daysCountInCurrentMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
        const MonthName = now.toLocaleString('ru-ru', { month: 'long' }).replace(/^./, str => str.toUpperCase());
        const FirstDayOfMonth = new Date(now.getFullYear(), now.getMonth(), 1).getDay();

        const eventDates: string[] = Object.keys(calendarMiniDates);

        return {
            daysCountInCurrentMonth,
            currentYear,
            currentMonth,
            formatNumLength,
            MonthName,
            weekDays,
            FirstDayOfMonth,
            eventDates,
            calendarMiniDates
        }
    },
})

</script>
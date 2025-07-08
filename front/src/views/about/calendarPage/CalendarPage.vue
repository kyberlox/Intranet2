<template>
    <div class="page__title mt20">Календарь событий</div>
    <div class="calendar-container">
        <div class="calendar__meanings">
            <div class="calendar_meaning">Основные события
                <div class="square-mark"
                     style="background-color: #f36509"></div>
            </div>
            <div class="calendar_meaning">ОВК
                <div class="square-mark"
                     style="background-color: #00b38c">
                </div>
            </div>
        </div>
        <div class="datepicker__wrapper">
            <DatePicker month-picker
                        disable-year-select
                        :calendarType="'month'"
                        @clearValue="clearDatePicker"
                        @pickDate="(i) => handleMonthChange(i)" />
        </div>
    </div>
    <div class="calendarYear mt20"
         v-if="currentEvents">
        <div class="calendarYear__item__wrapper"
             v-for="month in visibleMonthes"
             :key="'month' + month.value">
            <div class="calendarYear__item">
                <div class="calendarYear__title "
                     :class="{ 'calendarYear__title--target': String(monthId) == month.value }"
                     :data-month-num="month.value"
                     ref=chosenMonth>{{ month.name }}</div>
                <div class="calendarYear__content">
                    <div class="calendarYear__event__wrapper"
                         v-for="event in getEventFromMonth(month.value)"
                         :key="event.id">
                        <div class="calendarYear__event">
                            <div class="calendarYear__event__dates"
                                 v-if="event.DATE_FROM && event.DATE_TO && formatDateNoTime(event.DATE_FROM) !==
                                    formatDateNoTime(event.DATE_TO)">
                                <span class="calendarYear__event__date">
                                    {{
                                        formatDateNoTime(event.DATE_FROM) + ' - ' + formatDateNoTime(event.DATE_TO)
                                    }}
                                </span>
                            </div>
                            <div v-else
                                 class="calendarYear__event__date">
                                {{ event.DATE_FROM ? formatDateNoTime(event.DATE_FROM) : '' }}
                            </div>
                            <span class="calendarYear__event__name">
                                {{ event.NAME }}
                            </span>
                            <div class="square-mark"></div>
                            <a v-if="checkButtonStatus(event)"
                               class="calendarYear__event-btn"
                               :style="{ '--event-color': event.color }"
                               :class="[{ 'calendarYear__event-btn--ovk': event.CREATED_BY == '2857' }, { 'calendarYear__event-btn--dpm': event.CREATED_BY == '3542' && !event.COLOR }, { 'calendarYear__event-btn--custom-color': event.CREATED_BY == '3542' && event.COLOR }]"
                               :href="`https://portal.emk.ru/calendar/?EVENT_ID=${event.ID}EVENT_DATE=${event.DATE_FROM}`"
                               target="_blank">
                                {{ checkButtonStatus(event) }}
                            </a>
                            <span class="calendarYear__event-btn calendarYear__event-btn--no-border"
                                  v-else></span>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { monthesInit } from '@/assets/static/monthes';
import type { ICalendar } from '@/interfaces/ICalendar';
import DatePicker from '@/components/tools/common/DatePicker.vue';
import Api from '@/utils/Api';
import { dateConvert } from '@/utils/dateConvert';
import router from '@/router';

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
        const years = Object.keys([]);
        const currentYear = new Date().getFullYear();
        const currentEvents = ref();
        const visibleMonthes = ref(monthesInit);
        const router = useRouter();

        onMounted(() => {
            fetch(`https://portal.emk.ru/rest/1/f5ij1aoyuw5f39nb/calendar.event.get.json?type=company_calendar&ownerId=0&from=${currentYear}-01-01&to=${currentYear}-12-31`)
                .then((resp) => resp.json())
                .then((data) => {
                    currentEvents.value = data.result;
                });
        })

        const checkButtonStatus = (event: ICalendarEntity) => {
            if (event.DATE_FROM && event.ID) {
                return 'Подробнее'
            }
            else
                return false
        }
        const yearSelect = ref(new Date().getFullYear());

        const date = ref('');

        const chosenMonth = ref();

        watch((props), (newVal) => {
            if (newVal.monthId && chosenMonth.value) {
                chosenMonth.value.map((e: HTMLElement) => {
                    if (e.getAttribute('data-month-num') == props.monthId) {
                        setTimeout(() =>
                            e.scrollIntoView({ behavior: 'smooth', block: 'center' }), 10)
                    }
                })
            }
        })

        const getMonth = (date: string) => {
            return date.split('.')[1];
        }

        const formatDateNoTime = (date: string) => {
            return date.split(' ')[0];
        }

        const getEventFromMonth = (monthNum: string) => {
            const monthEvents = currentEvents.value.filter((e) => {
                return getMonth(formatDateNoTime(e.DATE_FROM)) == monthNum
            })
            return monthEvents.length ? monthEvents : [{ NAME: 'В этом месяце событий нет' }]
        }

        const handleMonthChange = (monthValue: { month: number, year: number }) => {
            visibleMonthes.value = monthesInit.filter((e) => {
                return Number(e.value) == monthValue.month + 1;
            })
        }

        const clearDatePicker = () => {
            router.push({ name: 'calendar' })
            visibleMonthes.value = monthesInit;
        }

        return {
            years,
            visibleMonthes,
            currentYear,
            yearSelect,
            currentEvents,
            checkButtonStatus,
            date,
            getMonth,
            chosenMonth,
            formatDateNoTime,
            getEventFromMonth,
            handleMonthChange,
            clearDatePicker,
        };
    },
});
</script>

<style lang="scss">
.calendarYear__title--target {
    background-color: rgba(0, 123, 255, 0.1);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #007bff;
    transition: all 0.3s ease;
}

.calendarYear__event {
    border-bottom: 1px solid rgba(146, 140, 140, 0.237);
    min-height: 69px;
}

.calendarYear__event__dates {
    display: flex;
    flex-direction: column;
    gap: 2px;
    align-items: center;
}

.calendarYear__event__date {
    max-width: 175px;
    min-width: 175px;
}

.calendarYear__event-btn {
    text-align: center;

    border: 1px solid var(--event-color);

    &:hover {
        background: var(--event-color) !important;
    }
}

.calendarYear__event-btn--no-border {
    border: none;
}

.dp--year-mode-picker {
    display: none;
}

.datepicker__wrapper {
    width: 100%;
    display: flex;
    flex-direction: row;
}

.dp__icon {
    color: var(--emk-brand-color);
}


.calendarYear__event-btn--ovk {
    border: 1px solid #00b38c;


    &:hover {
        background: #00b38c;
    }
}

.calendarYear__event-btn--dpm {
    border: 1px solid #f36509;

    &:hover {
        background: #f36509;
    }
}
</style>
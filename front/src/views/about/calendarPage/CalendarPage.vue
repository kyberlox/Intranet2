<template>
    <div class="page__content"
         v-if="currentEvents?.length">
        <div class="page__title mt20">Календарь событий</div>
        <div class="calendar-container">
            <!-- <div class="calendar__meanings">
                <div class="calendar_meaning">Основные события
                    <div class="square-mark"
                         style="background-color: #f36509"></div>
                </div>
                <div class="calendar_meaning">ОВК
                    <div class="square-mark"
                         style="background-color: #00b38c">
                    </div>
                </div>
            </div> -->
            <div class="datepicker__wrapper">
                <DatePicker month-picker
                            disable-year-select
                            :calendarType="'month'"
                            @clearValue="visibleMonthes = monthesInit"
                            @pickDate="handleMonthChange" />
            </div>
        </div>
        <div class="calendarYear mt20"
             v-if="currentEvents">
            <div class="calendarYear__item__wrapper"
                 v-for="month in visibleMonthes"
                 :key="'month' + month.value">
                <div class="calendarYear__item">
                    <div class="calendarYear__title "
                         :class="{ 'calendarYear__title--target': String(targetId) == month.value }"
                         :data-month-num="month.value"
                         ref=monthNodes>
                        {{ month.name }}
                    </div>
                    <div class="calendarYear__content">
                        <div class="calendarYear__event__wrapper"
                             v-for="(event, index) in getEventFromMonth(month.value)"
                             :key="'event' + index">
                            <div class="calendarYear__event"
                                 ref=eventNodes
                                 :class="{ 'calendarYear__event--chosen': isCalendarEvent(event) && event.DATE_FROM && targetId == event.ID }"
                                 :style="{ '--event-color': isCalendarEvent(event) && event.COLOR || '#f36509' }"
                                 :data-event-id="'ID' in event ? event.ID : ''"
                                 :data-date-target="'DATE_TO' in event ? event.DATE_TO : ''">
                                <div class="calendarYear__event__dates"
                                     v-if="isCalendarEvent(event) && event.DATE_FROM && event.DATE_TO && formatDateNoTime(event.DATE_FROM) !==
                                        formatDateNoTime(event.DATE_TO)">
                                    <span class="calendarYear__event__date">
                                        {{
                                            formatDateNoTime(event.DATE_FROM) + ' - ' + formatDateNoTime(event.DATE_TO)
                                        }}
                                    </span>
                                </div>
                                <div v-else
                                     class="calendarYear__event__date">
                                    {{ formatDateNoTime('DATE_FROM' in event ? event.DATE_FROM : '') }}
                                </div>
                                <span class="calendarYear__event__name">
                                    {{ event.NAME }}
                                </span>
                                <div class="square-mark"></div>
                                <a v-if="isCalendarEvent(event) && checkButtonStatus(event)"
                                   class="calendarYear__event-btn"
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
    </div>
</template>
<script lang="ts">
import { computed, defineComponent, onMounted, ref, watch, nextTick, type ComputedRef, type Ref } from 'vue';
import { monthesInit } from '@/assets/static/monthes';
import type { ICalendar } from '@/interfaces/entities/ICalendar';
import DatePicker from '@/components/tools/common/DatePicker.vue';
import { getMonth, formatDateNoTime } from '@/utils/dateConvert';
import { useViewsDataStore } from '@/stores/viewsData';

export default defineComponent({
    components: {
        DatePicker
    },
    props: {
        targetId: {
            type: String
        },
    },
    setup(props) {
        const visibleMonthes = ref(monthesInit);
        const date = ref('');
        const monthNodes = ref();
        const eventNodes = ref();
        const currentEvents: ComputedRef<ICalendar[]> = computed(() => useViewsDataStore().getData('calendarData') as ICalendar[]);

        const isCalendarEvent = (event: ICalendar | { NAME: string }): event is ICalendar => {
            return 'DATE_FROM' in event;
        };

        const checkButtonStatus = (event: ICalendar) => {
            if (event.DATE_FROM && event.ID) {
                return 'Подробнее'
            }
            else
                return false
        }

        const scrollToNode = async (target: string, nodes: Ref<HTMLElement[]>, attrTitle: string) => {
            console.log(target, nodes.value?.length, !attrTitle);

            await nextTick()

            if (!target || !nodes.value?.length || !attrTitle) return;
            visibleMonthes.value = monthesInit;

            nodes.value.map((e: HTMLElement) => {
                if (e.getAttribute(attrTitle) == target) {
                    setTimeout(() =>
                        e.scrollIntoView({ behavior: 'smooth', block: 'center' }), 100)
                }
            })
        }

        watch((props), () => {
            visibleMonthes.value = monthesInit;
            if (props.targetId) {
                scrollToNode(props.targetId, eventNodes, 'data-event-id')
            }
        }, { immediate: true, deep: true })

        const getEventFromMonth = (monthNum: string) => {
            const monthEvents = currentEvents.value.filter((e) => {
                const newDate = formatDateNoTime(e.DATE_FROM);
                if (!newDate) return;
                return getMonth(newDate) == monthNum
            })

            return monthEvents.length ? monthEvents.sort((a, b) => (formatDateNoTime(a.DATE_FROM) ?? '1').localeCompare((formatDateNoTime(b.DATE_FROM) ?? '0'))) : [{ NAME: 'В этом месяце событий нет' }]
        }

        const handleMonthChange = (monthValue: { month: number, year: number }) => {
            visibleMonthes.value = monthesInit.filter((e) => {
                return Number(e.value) == monthValue.month + 1;
            })
        }

        return {
            visibleMonthes,
            monthesInit,
            currentEvents,
            date,
            monthNodes,
            eventNodes,
            checkButtonStatus,
            getMonth,
            formatDateNoTime,
            getEventFromMonth,
            handleMonthChange,
            isCalendarEvent
        };
    },
});
</script>
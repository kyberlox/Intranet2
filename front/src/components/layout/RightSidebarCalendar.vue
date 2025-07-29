<template>
    <div class="calendar__wrapper">
        <DatePicker inline
                    v-model="date"
                    @date-update="dateClicked"
                    :markers="markers"
                    calendarType="monthAndYear" />
        <div class="calendar__button__wrapper">
            <div @click="handleRouteToCurrentMonth"
                 class="primary-button">
                Все события
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, ref, type Ref, computed, type ComputedRef, watch } from 'vue';
import DatePicker from '../tools/common/DatePicker.vue';
import { dateConvert, formatDateNoTime, addZeroToMonth } from '@/utils/dateConvert';
import { useRouter, useRoute } from 'vue-router';
import type { ICalendar } from '@/interfaces/entities/ICalendar';
import { useViewsDataStore } from '@/stores/viewsData';

interface ICalendarMarker {
    color?: string,
    date?: Date,
    type?: string,
    tooltip?: {
        text?: string,
        color?: string
    }[]
}

export default defineComponent({
    components: { DatePicker },
    setup() {
        const markers: Ref<ICalendarMarker[]> = ref([]);
        const route = useRoute();
        const router = useRouter();
        const viewsStore = useViewsDataStore();
        const date = ref(new Date());

        const calendarData: ComputedRef<ICalendar[]> = computed(() => viewsStore.getData('calendarData') as ICalendar[]);

        const formatDateDMY = (dateString: string): Date => {
            const [datePart, timePart] = dateString.split(' ');
            const [day, month, year] = datePart.split('.');
            return new Date(timePart ? `${month}/${day}/${year} ${timePart}` : `${month}/${day}/${year}`);
        };

        const generateDateRange = (startDate: string, endDate: string): Date[] => {
            const dates: Date[] = [];
            const currentDate = formatDateDMY(startDate);
            const endDateObj = formatDateDMY(endDate);

            while (currentDate <= endDateObj) {
                dates.push(new Date(currentDate));
                currentDate.setDate(currentDate.getDate() + 1);
            }

            return dates;
        };

        const createMarker = (
            date: Date,
            type: string,
            event: ICalendar
        ): ICalendarMarker => ({
            date: new Date(date),
            type,
            tooltip: [{ text: event.NAME || '', color: event.COLOR || 'orange' }],
            color: event.COLOR || 'orange'
        });

        const createCalendarEvent = (event: ICalendar): ICalendarMarker[] => {
            const eventMarkers: ICalendarMarker[] = [];

            if (!event.DATE_FROM) return eventMarkers;

            const formattedStartDate = formatDateNoTime(event.DATE_FROM);
            if (!formattedStartDate) return eventMarkers;

            const startDate = new Date(dateConvert(formattedStartDate, 'toDateType'));

            eventMarkers.push(createMarker(startDate, 'dot', event));

            if (event.DATE_TO && formatDateNoTime(event.DATE_FROM) !== formatDateNoTime(event.DATE_TO)) {
                const dateRange = generateDateRange(event.DATE_FROM, event.DATE_TO);

                dateRange.forEach((date) => {
                    const currentDateFormatted = dateConvert(String(date), 'toStringType');

                    const dotType = (currentDateFormatted == formatDateNoTime(event.DATE_TO) || currentDateFormatted == formatDateNoTime(event.DATE_FROM));

                    const markerType = dotType ? 'dot' : 'line';

                    eventMarkers.push(createMarker(date, markerType, event));
                });
            }
            return eventMarkers;
        };


        const dateClicked = (pickedDate: string) => {
            const target = calendarData.value.find((event) =>
                formatDateNoTime(event.DATE_FROM) === dateConvert(pickedDate, 'toStringType')
            );

            if (!target) return;

            const targetDate = formatDateNoTime(target.DATE_FROM);
            if (route.params?.date !== targetDate) {
                router.push({
                    name: 'calendarMonth',
                    params: { date: targetDate }
                });
            }
        };

        const handleRouteToCurrentMonth = () => {
            const currentMonth = addZeroToMonth(String(new Date().getMonth()));
            router.push({ name: 'calendar' });
            setTimeout(() =>
                router.push({ name: 'calendarMonth', params: { monthId: currentMonth } }), 30)
        }

        return {
            date,
            markers,
            dateClicked,
            addZeroToMonth,
            handleRouteToCurrentMonth,
        }
    },
})

</script>
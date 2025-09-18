<template>
    <div class="calendar__wrapper">
        <DatePicker inline
                    v-model="date"
                    @markerClick="(item: ICalendarMarker) => dateClicked(item)"
                    :markers="markers"
                    calendarType="monthAndYear">
        </DatePicker>
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
import { dateConvert, formatDateNoTime } from '@/utils/dateConvert';
import { useRoute, useRouter } from 'vue-router';
import { useViewsDataStore } from '@/stores/viewsData';

import type { ICalendar } from '@/interfaces/IEntities';

export interface ICalendarMarker {
    color?: string,
    date?: Date,
    type?: string,
    tooltip?: {
        text?: string,
        color?: string
    }[],
    ID: string,
    DATE_FROM: string,
    DATE_TO: string | null
}

export default defineComponent({
    components: { DatePicker },
    setup() {
        const markers: Ref<ICalendarMarker[]> = ref([]);
        const router = useRouter();
        const viewsStore = useViewsDataStore();
        const date = ref(new Date());
        const route = useRoute();

        const calendarData: ComputedRef<ICalendar[]> = computed(() => viewsStore.getData('calendarData') as ICalendar[]);

        const createMarker = (
            date: Date,
            type: string,
            event: ICalendar,
        ): ICalendarMarker => ({
            date: new Date(date),
            type,
            tooltip: [{ text: event.NAME || '', color: event.COLOR || 'orange' }],
            color: event.COLOR || 'orange',
            DATE_FROM: event.DATE_FROM,
            ID: event.ID,
            DATE_TO: event.DATE_TO ?? null
        });

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

        const createCalendarEvent = (event: ICalendar) => {
            if (!event.DATE_FROM) return;

            const formattedStartDate = formatDateNoTime(event.DATE_FROM);
            if (!formattedStartDate) return;

            const startDate = new Date(dateConvert(formattedStartDate, 'toDateType'));

            markers.value.push(createMarker(startDate, 'dot', event));

            if (event.DATE_TO && formatDateNoTime(event.DATE_FROM) !== formatDateNoTime(event.DATE_TO)) {
                const dateRange = generateDateRange(event.DATE_FROM, event.DATE_TO);

                dateRange.forEach((date) => {
                    const currentDateFormatted = dateConvert(String(date), 'toStringType');

                    const dotType = (currentDateFormatted == formatDateNoTime(event.DATE_TO) || currentDateFormatted == formatDateNoTime(event.DATE_FROM));

                    const markerType = dotType ? 'dot' : 'line';

                    markers.value.push(createMarker(date, markerType, event));
                });
            }
        };

        watch((calendarData), (newVal) => {
            if (!newVal) return;
            newVal.map((e) => {
                createCalendarEvent(e);
            })
        }, { immediate: true, deep: true })

        const dateClicked = (marker: ICalendarMarker) => {
            const target = marker.ID;
            if (!target || route.params.targetId == target) return;
            router.push({
                name: 'calendarMonth',
                params: { targetId: target }
            });
        };

        const handleRouteToCurrentMonth = () => {
            router.push({ name: 'calendar' });
            setTimeout(() =>
                router.push({ name: 'calendarMonth' }), 30)
        }

        return {
            date,
            markers,
            dateClicked,
            handleRouteToCurrentMonth,
        }
    },
})

</script>
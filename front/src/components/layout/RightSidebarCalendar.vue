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
import type { ICalendar } from '@/interfaces/ICalendar';
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

        watch((calendarData), (newVal) => {
            if (newVal && newVal.length) {
                calendarData.value.forEach((e) => {
                    // Создаю маркеры для vueDatePicker
                    const markerItem: Ref<ICalendarMarker> = ref({});

                    if (!e.DATE_FROM) return;
                    const formatedDate = formatDateNoTime(e.DATE_FROM);
                    if (!formatedDate) return;

                    markerItem.value.date = new Date(dateConvert(formatedDate, 'toDateType'));
                    markerItem.value.type = 'dot';
                    markerItem.value.tooltip = [{ text: e.NAME || '', color: e.COLOR || 'orange' }];
                    markerItem.value.color = e.COLOR || 'orange';
                    markers.value.push(markerItem.value);
                });
            }
        }, { immediate: true, deep: true })


        const dateClicked = (pickedDate: string) => {
            const target = calendarData.value.find((e) => formatDateNoTime(e.DATE_FROM) == dateConvert(pickedDate, 'toStringType'));
            if (!target) return;
            if (route.params && route.params.date !== formatDateNoTime(target.DATE_FROM)) {
                router.push({ name: 'calendarMonth', params: { date: formatDateNoTime(target.DATE_FROM) } })
            }
        }

        const handleRouteToCurrentMonth = () => {
            router.push({ name: 'calendar' });
            setTimeout(() =>
                router.push({ name: 'calendarMonth', params: { monthId: addZeroToMonth(String(new Date().getMonth())) } }), 30)
        }
        return {
            date,
            markers,
            dateClicked,
            addZeroToMonth,
            handleRouteToCurrentMonth
        }
    },
})

</script>
<template>
    <div class="calendar__wrapper">
        <DatePicker inline
                    v-model="date"
                    @date-update="dateClicked"
                    :markers="markers"
                    calendarType="monthAndYear" />
        <div class="calendar__button__wrapper">
            <RouterLink v-if="true"
                        :to="{ name: 'calendarMonth', params: { monthId: new Date().getMonth() + 1 } }"
                        class="primary-button">
                Все события
            </RouterLink>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, ref, type Ref, computed, type ComputedRef, watch } from 'vue';
import DatePicker from '../tools/common/DatePicker.vue';
import { dateConvert, formatDateNoTime } from '@/utils/dateConvert';
import { useRouter } from 'vue-router';
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
        const router = useRouter();
        const viewsStore = useViewsDataStore();

        const calendarData: ComputedRef<ICalendar[]> = computed(() => viewsStore.getData('calendarData') as ICalendar[]);

        watch((calendarData), (newVal) => {
            if (newVal && newVal.length) {
                calendarData.value.forEach((e) => {
                    // Создаю маркеры для vueDatePicker
                    const markerItem: Ref<ICalendarMarker> = ref({});


                    // if (typeof newDate !== 'string') return;
                    // markerItem.value.date = new Date('01.01.2025');
                    console.log(formatDateNoTime(e.DATE_FROM));

                    if (!e.DATE_FROM) return;
                    markerItem.value.date = new Date(dateConvert(formatDateNoTime(e.DATE_FROM), 'toDateType'));
                    console.log(markerItem.value.date);
                    markerItem.value.type = 'dot';
                    markerItem.value.tooltip = [{ text: e.NAME || '', color: e.COLOR || 'orange' }];
                    markerItem.value.color = e.COLOR || 'orange';
                    markers.value.push(markerItem.value);
                });
            }
        }, { immediate: true, deep: true })



        const date = ref(new Date());

        const dateClicked = (pickedDate: string) => {
            const target = calendarData.value.find((e) => String(e.DATE_TO) == dateConvert(pickedDate, 'toStringType'));
            if (!target) return;
            router.push({ name: 'calendarMonth', params: { monthId: target.DATE_TO.split('.')[1] } })
        }


        return {
            date,
            markers,
            dateClicked,
        }
    },
})

</script>

<style>
.dp__tooltip_text {
    display: flex;
    flex-direction: column;
    width: 250px !important;
    word-break: break-word;

    white-space: normal;

    overflow-wrap: break-word;

}
</style>
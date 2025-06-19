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
import { defineComponent, onMounted, ref, type Ref } from 'vue';
import { calendarMiniDates } from '@/assets/staticJsons/calendar';
import DatePicker from '../tools/common/DatePicker.vue';
import { dateConvert } from '@/utils/dateConvert';
import { useRouter } from 'vue-router';

interface CalendarEvent {
    id?: string;
    month?: string;
    past?: boolean;
    name?: string;
    calendar_id?: string;
    report?: {
        ELEMENT_ID: string;
        NAME: string;
        URL: string;
    } | false;
    preview?: {
        ELEMENT_ID: string;
        NAME: string;
        URL: string;
    } | false;
    private_event?: string;
    attendee_status?: string | null;
    entryId?: string | null;
    date: string,
    type?: string,
    color?: string,
    tooltip?: { text: string, color: string }[]
}

export default defineComponent({
    components: { DatePicker },
    setup() {
        const markers: Ref<CalendarEvent[]> = ref([]);
        const router = useRouter();
        const calendarPlug: CalendarEvent[] = [
            {
                "id": "101575",
                "month": "01",
                "date": "29.01.2025",
                "past": true,
                "name": "V турнир по боулингу ЭМК",
                "calendar_id": "1949",
                "report": {
                    "ELEMENT_ID": "23393",
                    "NAME": "«Экспортанцы» вернули себе звание чемпионов боулинга.",
                    "URL": "/intranet/company-life/news/?ELEMENT_ID=23393"
                },
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": "N",
                "entryId": "102481"
            },
            {
                "id": "124647",
                "month": "03",
                "date": "02.03.2025",
                "past": true,
                "name": "Масленица ЭМК",
                "calendar_id": "1949",
                "report": {
                    "ELEMENT_ID": "27028",
                    "NAME": "В ЭМК ярко и весело проводили Масленицу.",
                    "URL": "/intranet/company-life/news/?ELEMENT_ID=27028"
                },
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": "N",
                "entryId": "125546"
            },
            {
                "id": "128279",
                "month": "03",
                "date": "15.03.2025",
                "past": true,
                "name": "Weekend в Хвалынске",
                "calendar_id": "1949",
                "report": {
                    "ELEMENT_ID": "29106",
                    "NAME": "Weekend в Хвалынске прошел в ЭМК.",
                    "URL": "/intranet/company-life/news/?ELEMENT_ID=29106"
                },
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": "Q",
                "entryId": "129178"
            },
            {
                "id": "126200",
                "month": "03",
                "date": "22.03.2025",
                "past": true,
                "name": "II Кибертурнир",
                "calendar_id": "1949",
                "report": {
                    "ELEMENT_ID": "29894",
                    "NAME": "В ЭМК состоялся II корпоративный кибертурнир.",
                    "URL": "/intranet/company-life/news/?ELEMENT_ID=29894"
                },
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": "N",
                "entryId": "127100"
            },
            {
                "id": "135472",
                "month": "04",
                "date": "04.04.2025",
                "past": true,
                "name": "Квиз",
                "calendar_id": "1949",
                "report": {
                    "ELEMENT_ID": "31633",
                    "NAME": "В ЭМК определены победители Квиза.",
                    "URL": "/intranet/company-life/news/?ELEMENT_ID=31633"
                },
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": "N",
                "entryId": "136377"
            },
            {
                "id": "103630",
                "month": "04",
                "date": "14.04.2025",
                "past": true,
                "name": "Нефтегаз",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": "N",
                "entryId": "104676"
            },
            {
                "id": "143363",
                "month": "04",
                "date": "15.04.2025",
                "past": true,
                "name": "Нефтегаз",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "143365",
                "month": "04",
                "date": "16.04.2025",
                "past": true,
                "name": "Нефтегаз",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "143367",
                "month": "04",
                "date": "17.04.2025",
                "past": true,
                "name": "Нефтегаз",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "137735",
                "month": "04",
                "date": "17.04.2025",
                "past": true,
                "name": "Мастер-класс по танцам",
                "calendar_id": "1949",
                "report": {
                    "ELEMENT_ID": "33231",
                    "NAME": "В ЭМК прошел мастер-класс по танцам. ",
                    "URL": "/intranet/company-life/news/?ELEMENT_ID=33231"
                },
                "preview": false,
                "color": "#00b38c",
                "private_event": "",
                "attendee_status": "N",
                "entryId": "138639"
            },
            {
                "id": "140408",
                "month": "04",
                "date": "19.04.2025",
                "past": true,
                "name": "Велопрогулка",
                "calendar_id": "1949",
                "report": {
                    "ELEMENT_ID": "33376",
                    "NAME": "Велосипедная прогулка ЭМК на Кумысной поляне!",
                    "URL": "/intranet/company-life/news/?ELEMENT_ID=33376"
                },
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": "Q",
                "entryId": "141313"
            },
            {
                "id": "127714",
                "month": "04",
                "date": "27.04.2025",
                "past": true,
                "name": "День основания НПО \"Регулятор\"",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "103628",
                "month": "05",
                "date": "13.05.2025",
                "past": true,
                "name": "Выставка OGU",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "144827",
                "month": "05",
                "date": "17.05.2025",
                "past": true,
                "name": "Экскурсия в питомник хаски",
                "calendar_id": "1949",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": "Q",
                "entryId": "145730"
            },
            {
                "id": "149615",
                "month": "05",
                "date": "23.05.2025",
                "past": true,
                "name": "Весенняя корпоративная конференция",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "103632",
                "month": "05",
                "date": "28.05.2025",
                "past": true,
                "name": "Иннопром",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "146901",
                "month": "05",
                "date": "30.05.2025",
                "past": true,
                "name": "Квартирник ЭМК",
                "calendar_id": "1949",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "127889",
                "month": "06",
                "date": "05.06.2025",
                "past": false,
                "name": "Курганский форум",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "150970",
                "month": "06",
                "date": "07.06.2025",
                "past": false,
                "name": "VIII рыболовный турнир ЭМК",
                "calendar_id": "1949",
                "report": false,
                "preview": {
                    "ELEMENT_ID": "36267",
                    "NAME": "VIII рыболовный турнир ЭМК. ",
                    "URL": "/intranet/company-life/poster/?ELEMENT_ID=36267"
                },
                "color": "",
                "private_event": "",
                "attendee_status": "Q",
                "entryId": "151869"
            },
            {
                "id": "127891",
                "month": "06",
                "date": "27.06.2025",
                "past": false,
                "name": "Семинар ЭМК в г. Нижнекамске",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "127906",
                "month": "07",
                "date": "18.07.2025",
                "past": false,
                "name": "Семинар ЭМК в г. Мурманск",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "127909",
                "month": "08",
                "date": "01.08.2025",
                "past": false,
                "name": "Семинар ЭМК в г. Новороссийск",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "103641",
                "month": "08",
                "date": "21.08.2025",
                "past": false,
                "name": "Слёт проектировщиков",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "127911",
                "month": "09",
                "date": "05.09.2025",
                "past": false,
                "name": "Семинар ЭМК в г. Казань",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "103645",
                "month": "09",
                "date": "26.09.2025",
                "past": false,
                "name": "Осенняя корпоративная конференция",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "127913",
                "month": "09",
                "date": "29.09.2025",
                "past": false,
                "name": "ИННОПРОМ",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "103626",
                "month": "10",
                "date": "07.10.2025",
                "past": false,
                "name": "Газовый форум",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            },
            {
                "id": "103636",
                "month": "11",
                "date": "25.11.2025",
                "past": false,
                "name": "Выставка PulpFor",
                "calendar_id": "47",
                "report": false,
                "preview": false,
                "color": "",
                "private_event": "",
                "attendee_status": null,
                "entryId": null
            }
        ]
        onMounted(() => {
            calendarPlug.forEach((e: CalendarEvent) => {
                const markerItem: CalendarEvent = { ...e };
                if (!markerItem) return;
                const newDate = dateConvert(e.date, 'toDateType');
                if (typeof newDate !== 'string') return;
                markerItem.date = newDate;
                markerItem.type = 'dot';
                markerItem.tooltip = [{ text: e.name || '', color: e.color || 'orange' }];
                markerItem.color = e.color || 'orange';

                markers.value.push(markerItem);
            });
        })

        const date = ref(new Date());

        const dateClicked = (pickedDate: string) => {
            const target = calendarPlug.find((e) => String(e.date) == dateConvert(pickedDate, 'toStringType'));
            if (!target) return;
            router.push({ name: 'calendarMonth', params: { monthId: target.date.split('.')[1] } })
        }

        return {
            calendarMiniDates,
            date,
            markers,
            dateClicked,
        }
    },
})

</script>
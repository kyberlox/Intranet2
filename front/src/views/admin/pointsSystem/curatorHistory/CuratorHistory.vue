<template>
<div>
    <div class="tags__page__filter"
         v-if="filters && Object.keys(filters).length">
        <div v-for="(item) in Object.keys(filters)"
             :key="'filter' + item.length">
            <button @click="handleFilterChange(item)"
                    class="btn dropdown-toggle tagDateNavBar__dropdown-toggle">
                {{ setButtonText(item) }}
            </button>
            <CustomFilter v-if="showFilter.includes(item)"
                          :params="filters[item as keyof typeof filters]"
                          :buttonText="filterChoices[item as keyof typeof filterChoices]"
                          @pickFilter="(filter: string) => pickFilter(filter, (item as ('activity_name' | 'uuid_to_fio')))" />
        </div>
        <div class="calendar-container">
            <div class="dp__wrapper">
                <DatePicker range
                            :calendarType="'fullNoYear'"
                            :disable-year-select="false"
                            @clearValue="{ dateFilter = ''; tableInit() }"
                            @pickDate="changeDateFilter" />
            </div>
        </div>
    </div>
    <PointsHistoryActionTable :needCheckButton="false"
                              :onlyHistory="true"
                              :activitiesInTable="activitiesInTable.filter((e) => filterNodes(e))"
                              @moderate="moderate" />
</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import PointsHistoryActionTable from '../PointsHistoryActionTable.vue';
import type { ICuratorActivityHistory } from '@/interfaces/IEntities';
import Api from '@/utils/Api';
import CustomFilter from '@/components/tools/common/CustomFilter.vue';
import DatePicker from '@/components/tools/common/DatePicker.vue';
import { dateConvert } from '@/utils/dateConvert';

export default defineComponent({
    components: {
        PointsHistoryActionTable,
        CustomFilter,
        DatePicker,
    },
    props: {
        needFilter: {
            type: Boolean,
            default: () => false
        }
    },
    setup() {
        const activitiesInTable = ref<ICuratorActivityHistory[]>([]);
        const showFilter = ref<string[]>([]);
        const dateFilter = ref();

        const filters = ref<{
            activity_name?: string[], uuid_to_fio?: string[]
        }>();
        const filterChoices = ref<{ activity_name: string, uuid_to_fio: string }>({
            activity_name: '',
            uuid_to_fio: ''
        });

        onMounted(() => {
            tableInit();
        })

        const moderate = (a: string, actionId: number, uuid: number, valid?: number) => {
            Api.post(`peer/remove_user_points/${uuid}/${actionId}/${valid}`)
                .finally(() => tableInit())
        }

        const tableInit = () => {
            Api.get('peer/get_curators_history')
                .then((data: ICuratorActivityHistory[]) => activitiesInTable.value = data)
                .finally(() => filters.value = getFilterTypes(activitiesInTable.value))
        }

        const getFilterTypes = (data: ICuratorActivityHistory[]) => {
            const filterKeys = ["activity_name", "uuid_to_fio"] as const;
            const filterObject: { activity_name: string[], uuid_to_fio: string[] } = {
                activity_name: [],
                uuid_to_fio: [],
            };
            filterKeys.forEach((e) => {
                data.forEach((i) => {
                    if (filterObject[e].includes(String(i[e as keyof typeof i]))) {
                        return
                    }
                    else {
                        filterObject[e].push(String(i[e as keyof typeof i]))
                    }
                })
            })
            return filterObject
        }

        const pickFilter = (filter: string, item: keyof typeof filterChoices.value) => {
            filterChoices.value[item] = filter;
            showFilter.value.length = 0;
        }

        const handleFilterChange = (item: string) => {
            if (!showFilter.value.includes(item)) {
                showFilter.value.length = 0;
                showFilter.value.push(item);
            }
            else
                showFilter.value.length = 0;
        }

        const filterNodes = (e: ICuratorActivityHistory) => {
            const compareDates = (e: ICuratorActivityHistory) => {
                if (!dateFilter.value) return true;
                if (Array.isArray(dateFilter.value) && dateFilter.value.length > 1) {
                    const formattedDate = (new Date(e.date_time)).getTime();
                    const firstDate = new Date(dateConvert(dateFilter.value[0], 'toDateType')).getTime();
                    const secDate = new Date(dateConvert(dateFilter.value[1], 'toDateType')).getTime();

                    if (formattedDate < firstDate || formattedDate > secDate) {
                        return false
                    }
                    else return true
                } else {
                    const formattedDate = dateConvert(String(new Date(e.date_time)), 'toStringType')
                    return formattedDate == dateFilter.value ? true : false;
                }
            }

            if ((e.activity_name == filterChoices.value.activity_name || !e.activity_name || !filterChoices.value.activity_name)
                && (e.uuid_to_fio == filterChoices.value.uuid_to_fio || !e.uuid_to_fio || !filterChoices.value.uuid_to_fio)
                && (compareDates(e))) {
                return true;
            }
            else return false
        }

        const changeDateFilter = (date: string) => {
            const newDate = Array.isArray(date) && dateConvert(date[0], 'toStringType') == dateConvert(date[1], 'toStringType') ? date[0] : date;
            dateFilter.value = Array.isArray(newDate) ? [dateConvert(newDate[0], 'toStringType'), dateConvert(newDate[1], 'toStringType')]
                : dateFilter.value = dateConvert(newDate, 'toStringType');
        }

        const setButtonText = (title: string) => {
            switch (title) {
                case 'activity_name':
                    return filterChoices.value.activity_name ? filterChoices.value.activity_name : 'Название'
                case 'uuid_to_fio':
                    return filterChoices.value.uuid_to_fio ? filterChoices.value.uuid_to_fio : 'Кому'
                default:
                    return 'Фильтр';
            }
        }

        return {
            activitiesInTable,
            showFilter,
            filterChoices,
            filters,
            dateFilter,
            handleFilterChange,
            moderate,
            filterNodes,
            pickFilter,
            changeDateFilter,
            tableInit,
            setButtonText
        }
    }
})
</script>
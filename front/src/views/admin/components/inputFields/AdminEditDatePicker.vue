<template>
<div class="admin-element-inner__field-content admin-element-inner__field-content--no-transition">
    <p class="admin-element-inner__field-title fs-l">
        {{ item?.name }}
    </p>
    <DatePicker class="admin-element-inner__date-picker"
                :disable-year-select="false"
                :timePicker="true"
                :calendarType="'full'"
                :defaultData="(value as string)"
                :item="item"
                @pickDate="(date: string) => handleValuePick(date)"
                @clearValue="() => handleValuePick(null)" />
</div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from 'vue';
import { useDateFormat } from '@vueuse/core';
import DatePicker from '@/components/tools/common/DatePicker.vue';
import type { IAdminListItem } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        DatePicker
    },
    props: {
        item: {
            type: Object as PropType<IAdminListItem>
        }
    },
    setup(props, { emit }) {
        const value = ref(props.item?.value);

        const handleValuePick = (date: string | null) => {
            if (date == null) {
                emit('pick', date)
            }
            else
                if (props.item?.field?.includes('from') || props.item?.field?.includes('to')) {
                    emit('pick', useDateFormat(date as string, 'DD.MM.YYYY'))
                }
                else {
                    emit('pick', useDateFormat(date as string, 'DD.MM.YYYY HH:mm:ss'))
                }
        }

        return {
            value,
            handleValuePick,
            useDateFormat
        }
    }
})
</script>

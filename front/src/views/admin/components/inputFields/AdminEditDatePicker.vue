<template>
<div class="admin-element-inner__field-content admin-element-inner__field-content--no-transition">
    <p class="admin-element-inner__field-title fs-l">{{ item?.name }}</p>
    <DatePicker class="admin-element-inner__date-picker"
                :disable-year-select="false"
                :timePicker="true"
                :calendarType="'full'"
                :defaultData="(item?.value as string)"
                @pickDate="(date: string) => { handleValuePick(useDateFormat(date, 'YYYY-MM-DD HH:mm:ss')) }"
                @clearValue="() => defaultValue = ''" />
</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, type PropType, ref } from 'vue';
import { useDateFormat, type UseDateFormatReturn } from '@vueuse/core';
import DatePicker from '@/components/tools/common/DatePicker.vue';
import type { IAdminListItem } from '@/interfaces/IEntities';
import { dateConvert } from '@/utils/dateConvert';

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
        const currentDate = `${dateConvert(String(new Date()), 'toStringType')} ${String(new Date()).split(' ')[4]}`;
        const defaultValue = ref(props.item?.value ? props.item.value : currentDate);

        const handleValuePick = (date: string | UseDateFormatReturn) => emit('pick', date);

        onMounted(() => {
            handleValuePick(defaultValue.value as string)
        })

        return {
            defaultValue,
            handleValuePick,
            useDateFormat,
        }
    }
})
</script>
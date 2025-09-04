<template>
    <div class="admin-element-inner__field-content admin-element-inner__field-content--no-transition">
        <p class="admin-element-inner__field-title fs-l">{{ item?.name }}</p>
        <DatePicker class="admin-element-inner__date-picker"
                    :disable-year-select="false"
                    :calendarType="'full'"
                    :defaultData="(item?.value as string)"
                    @pickDate="(date: string) => { handleValuePick(useDateFormat(date, 'DD.MM.YYYY HH:mm:ss')) }"
                    @clearValue="() => value = ''" />
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from 'vue';
import { useDateFormat } from '@vueuse/core';
import DatePicker from '@/components/tools/common/DatePicker.vue';
import { type UseDateFormatReturn } from '@vueuse/core';
import type { IAdminListItem } from '@/interfaces/entities/IAdmin';

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

        return {
            value,
            handleValuePick: (date: UseDateFormatReturn) => emit('pick', date),
            useDateFormat
        }
    }
})
</script>
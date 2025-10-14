<template>
<div class="admin-element-inner__field-content">
    <p v-if="item?.name"
       class="admin-element-inner__field-title fs-l">
        {{ item?.name }}
    </p>
    <select v-if="item?.field !== 'bx_event'"
            class="admin-element-inner__select"
            @change="handleValuePick"
            v-model="value">
        <option class="admin-element-inner__select-option"
                v-for="(option, index) in item?.values"
                :value="(typeof option === 'string' || typeof option === 'boolean') ? option : option.value ? option.value : option.id"
                :key=index>
            {{ (typeof option === 'string' || typeof option === 'boolean' ? (yesOrNoFormat ?
                renderOptionText(option) : option) : option.name) }}
        </option>
    </select>

    <div v-else
         class="admin-element-inner__select__loader">
        <Loader v-if="!calendarOptions || !calendarOptions.length" />
        <select v-else
                class="admin-element-inner__select"
                @change="handleValuePick"
                v-model="value">
            <option class="admin-element-inner__select-option"
                    v-for="(option, index) in calendarOptions"
                    :key=index
                    :value="option">
                {{ option.NAME }}
            </option>
        </select>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, type PropType, ref, computed } from 'vue';
import type { IAdminListItem, ICalendar } from '@/interfaces/IEntities';
import { useViewsDataStore } from '@/stores/viewsData';
import Loader from '@/components/layout/Loader.vue';

export default defineComponent({
    name: 'AdminEditSelect',
    components: {
        Loader
    },
    props: {
        yesOrNoFormat: {
            type: Boolean,
            default: true
        },
        item: {
            type: Object as PropType<IAdminListItem>
        },
    },
    setup(props, { emit }) {
        const DataStore = useViewsDataStore();
        const value = ref(props.item?.value);

        onMounted(() => {
            if (value.value)
                emit('pick', value.value)
        })

        return {
            value,
            calendarOptions: computed(() => DataStore.getData('calendarData') as ICalendar[]),
            renderOptionText: (text: boolean | string) => { return (String(text) == 'true' ? 'Да' : 'Нет') },
            handleValuePick: () => { emit('pick', value.value) },
        }
    }
})
</script>
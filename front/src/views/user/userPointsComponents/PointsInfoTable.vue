<template>
<div v-if="pointsHistory.length">
    <table class="point-info__table">
        <thead>
            <tr>
                <th>Дата</th>
                <th>Активность</th>
                <th>Кто отправил</th>
                <th>Комментарий</th>
                <th>Баллов</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in pointsHistory"
                :key="item.id_activeusers">
                <td>{{ dateConvert(item.date_time, 'toStringType') }}</td>
                <td>{{ item.activity_name }}</td>
                <td>{{ item.fio_from }}</td>
                <td>{{ item.description }}</td>
                <td>{{ item.cost }}</td>
            </tr>
        </tbody>
        <tfoot></tfoot>
    </table>
</div>
<div class="point-info__table__slug"
     v-else>
    У вас пока нет начисленных баллов
</div>
</template>

<script lang="ts">
import { defineComponent, computed, type ComputedRef } from 'vue';
import { useUserScore } from '@/stores/userScoreData';
import type { IActivityStatistics } from '@/interfaces/IEntities';
import { dateConvert } from '@/utils/dateConvert';

export default defineComponent({
    name: 'pointsInfoTable',
    setup() {
        const pointsHistory: ComputedRef<IActivityStatistics[]> = computed(() => useUserScore().getStatistics)

        return {
            pointsHistory,
            dateConvert
        }
    }
})
</script>
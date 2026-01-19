<template>
<div v-if="pointsHistory.length">
    <table class="point-info__table">
        <thead>
            <tr>
                <th><span>Дата</span></th>
                <th><span>Активность</span></th>
                <th><span>Кто отправил</span></th>
                <th><span>Комментарий</span></th>
                <th><span>Баллов</span></th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in pointsHistory"
                :key="item.id_activeusers">
                <td><span>{{ dateConvert(item.date_time, 'toStringType') }}</span></td>
                <td><span>{{ item.activity_name }}</span></td>
                <td><span>{{ item.fio_from }}</span></td>
                <td><span>{{ item.description }}</span></td>
                <td><span>{{ item.cost }}</span></td>
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
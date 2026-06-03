<template>
<div v-if="pointsHistory.length">
    <table class="point-info__table">
        <thead>
            <tr>
                <th><span>Дата</span></th>
                <th><span>Название</span></th>
                <th><span>Кто отправил</span></th>
                <th><span>Комментарий</span></th>
                <th><span>Баллы</span></th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(item, index) in pointsHistory"
                :key="historyItemKey(item, index)">
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
    {{ emptyText }}
</div>
</template>

<script lang="ts">
import { defineComponent, computed, type PropType } from 'vue';
import { useUserScore } from '@/stores/userScoreData';
import type { IActivityStatistics } from '@/interfaces/IEntities';
import { dateConvert } from '@/utils/dateConvert';

type PointsHistoryType = 'addition' | 'purchase';
type PointsHistoryItem = IActivityStatistics & { id?: number };

export default defineComponent({
    name: 'pointsInfoTable',
    props: {
        historyType: {
            type: String as PropType<PointsHistoryType>,
            default: 'addition'
        }
    },
    setup(props) {
        const userScore = useUserScore();
        const pointsHistory = computed<IActivityStatistics[]>(() =>
            props.historyType === 'purchase' ? userScore.getPurchaseHistory : userScore.getAdditionHistory
        );
        const emptyText = computed(() =>
            props.historyType === 'purchase' ? 'У вас пока нет покупок в магазине мерча' : 'У вас пока нет начисленных баллов'
        );
        const historyItemKey = (item: PointsHistoryItem, index: number) => item.id_activeusers ?? item.id ?? `${item.date_time}-${index}`;

        return {
            pointsHistory,
            emptyText,
            historyItemKey,
            dateConvert
        }
    }
})
</script>

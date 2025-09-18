<template>
    <div>
        <table class="point-info__table">
            <thead>
                <tr>
                    <th>Дата</th>
                    <th>Кто отправил</th>
                    <th>Комментарий</th>
                    <th>Баллов</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in pointTablePlug"
                    :key="item.id">
                    <td>{{ item.date }}</td>
                    <td>{{ item.who }}</td>
                    <td>{{ item.comment }}</td>
                    <td>{{ item.score }}</td>
                </tr>
            </tbody>
            <tfoot></tfoot>
        </table>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'pointsInfoTable',

    setup() {
        const pointTablePlug = [
            {
                id: '1',
                date: '05.02.2024',
                who: 'Пользователь 1',
                param: 'Благодарность за экспертизу коллеги',
                comment: 'Консультация по сделке',
                score: '1',
            },
            {
                id: '2',
                date: '05.02.2024',
                who: 'Пользователь 2',
                param: 'Внешние мероприятия',
                comment: 'За участие в ПМГФ',
                score: '3',
            },
            {
                id: '3',
                date: '05.02.2024',
                who: 'Пользователь 3',
                param: 'Внутренние мероприятия',
                comment: 'За участие в масленице',
                score: '1',
            },
            {
                id: '4',
                date: '05.02.2024',
                who: 'Пользователь 4',
                param: 'Пройдено обучение',
                comment: 'Пройден курс 1-7',
                score: '21',
            },
        ]

        return {
            pointTablePlug
        }
    }
})
</script>
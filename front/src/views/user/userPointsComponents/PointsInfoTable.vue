<template>
    <div>
        <table>
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

<style lang="scss" scoped>
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    background-color: #fff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

    thead {
        background-color: #f8f9fa;

        th {
            padding: 16px 12px;
            text-align: left;
            font-weight: 600;
            color: #495057;
            border-bottom: 2px solid #e9ecef;

            &:first-child {
                padding-left: 20px;
            }

            &:last-child {
                padding-right: 20px;
                text-align: right;
            }
        }
    }

    tbody {
        tr {
            border-bottom: 1px solid #e9ecef;
            transition: background-color 0.2s ease;

            &:hover {
                background-color: #f8f9fa;
            }

            &:last-child {
                border-bottom: none;
            }

            td {
                padding: 14px 12px;
                color: #495057;
                vertical-align: top;

                &:first-child {
                    padding-left: 20px;
                    font-weight: 500;
                }

                &:last-child {
                    padding-right: 20px;
                    text-align: right;
                    font-weight: 600;
                    // color: var(--emk-brand-color);
                }
            }
        }
    }
}
</style>
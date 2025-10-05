<template>
<div v-if="activitiesInTable?.length"
     class="moderator-panel__content">
    <div class="moderator-panel__list">
        <div class="moderator-panel__table-item"
             v-for="item in activitiesInTable"
             :key="item.id">
            <table class="moderator-panel__table">
                <thead class="moderator-panel__thead">
                    <tr class="moderator-panel__row">
                        <th class="moderator-panel__head"
                            v-if="item.date_time">
                            Дата
                        </th>
                        <th v-if="'activity_name' in item"
                            class="moderator-panel__head">
                            Активность
                        </th>
                        <th class="moderator-panel__head"
                            v-if="('name' in (item))">
                            Параметр
                        </th>
                        <th class="moderator-panel__head"
                            v-if="'uuid_from' in item">
                            От кого
                        </th>
                        <th class="moderator-panel__head"
                            v-if="'uuid_to_fio' in item || 'uuid_to' in item">
                            Куда
                        </th>
                        <th class="moderator-panel__head"
                            v-if="item.description">
                            Комментарий
                        </th>
                        <th class="moderator-panel__head">
                            <CancelIcon v-if="!onlyHistory"
                                        @click="moderate('cancel', item.id, item.uuid_to)"
                                        class="moderator-panel__action-btn moderator-panel__action-btn--cancel" />
                        </th>
                    </tr>
                </thead>
                <tbody class="moderator-panel__tbody">
                    <tr class="moderator-panel__row">
                        <td v-if="item.date_time"
                            class="moderator-panel__cell moderator-panel__cell--date">
                            {{ dateConvert(item.date_time, 'toStringType') }}
                        </td>
                        <td v-if="'activity_name' in item"
                            class="moderator-panel__cell moderator-panel__cell--parameter">
                            {{ item.activity_name }}
                        </td>

                        <td v-if="'name' in item"
                            class="moderator-panel__cell moderator-panel__cell--parameter">
                            {{ item.name }}
                        </td>
                        <td v-if="'uuid_from' in item"
                            class="moderator-panel__cell moderator-panel__cell--from">
                            {{ item.uuid_from }}
                        </td>
                        <td v-if="'uuid_to_fio' in item"
                            class="moderator-panel__cell moderator-panel__cell--to">
                            {{ item.uuid_to_fio }}
                        </td>
                        <td v-else-if="item.uuid_to"
                            class="moderator-panel__cell moderator-panel__cell--to">
                            {{ item.uuid_to }}
                        </td>
                        <td class="moderator-panel__cell moderator-panel__cell--comment">
                            {{ item.description }}
                        </td>
                        <td class="moderator-panel__cell moderator-panel__cell--actions">
                            <CheckIcon v-if="!onlyHistory"
                                       @click="moderate('accept', item.id, item.uuid_to)"
                                       class="moderator-panel__action-btn moderator-panel__action-btn--accept" />
                        </td>
                    </tr>
                </tbody>
                <tfoot class="moderator-panel__tfoot"></tfoot>
            </table>
        </div>
    </div>
</div>
<div v-else>
    {{ onlyHistory ? 'У вас нет истории отправленных баллов' : 'Нет активностей на подтвержение' }}
</div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import { dateConvert } from '@/utils/dateConvert';
import CheckIcon from '@/assets/icons/common/Check.svg?component';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import type { IActivityToConfirm, ICuratorActivityHistory } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        CheckIcon,
        CancelIcon
    },
    props: {
        activitiesInTable: {
            type: Array as PropType<(IActivityToConfirm | ICuratorActivityHistory)[]>,
        },
        onlyHistory: {
            type: Boolean,
            default: () => false
        }
    },
    emits: ['moderate'],
    setup(_, { emit }) {

        return {
            dateConvert,
            moderate: (type: string, id: number, uuidTo: number) => emit('moderate', type, id, uuidTo),
        }
    }
})
</script>
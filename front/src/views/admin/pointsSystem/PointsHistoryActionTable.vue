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
                            <span>
                                Дата
                            </span>
                        </th>
                        <th v-if="'activity_name' in item"
                            class="moderator-panel__head">
                            <span>
                                Активность
                            </span>
                        </th>
                        <th v-if="'coast' in item"
                            class="moderator-panel__head">
                            <span>
                                Стоимость
                            </span>
                        </th>
                        <th class="moderator-panel__head"
                            v-if="('name' in (item))">
                            <span>
                                Параметр
                            </span>
                        </th>
                        <th class="moderator-panel__head"
                            v-if="'uuid_from' in item">
                            <span>
                                От кого
                            </span>
                        </th>
                        <th class="moderator-panel__head"
                            v-if="'uuid_to_fio' in item || 'uuid_to' in item">
                            <span>
                                Куда
                            </span>
                        </th>
                        <th class="moderator-panel__head"
                            v-if="item.description">
                            <span>
                                Комментарий
                            </span>
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
                            <span>
                                {{ dateConvert(item.date_time, 'toStringType') }}
                            </span>
                        </td>
                        <td v-if="'activity_name' in item"
                            class="moderator-panel__cell moderator-panel__cell--parameter">
                            <span>
                                {{ item.activity_name }}
                            </span>
                        </td>
                        <th v-if="'coast' in item"
                            class="moderator-panel__head">
                            <span>
                                {{ item.coast }}
                            </span>
                        </th>
                        <td v-if="'name' in item"
                            class="moderator-panel__cell moderator-panel__cell--parameter">
                            <span>
                                {{ item.name }}
                            </span>
                        </td>
                        <td v-if="'uuid_from' in item"
                            class="moderator-panel__cell moderator-panel__cell--from">
                            <span>
                                {{ item.uuid_from }}
                            </span>
                        </td>
                        <td v-if="'uuid_to_fio' in item"
                            class="moderator-panel__cell moderator-panel__cell--to">
                            <span>
                                {{ item.uuid_to_fio }}
                            </span>
                        </td>
                        <td v-else-if="item.uuid_to"
                            class="moderator-panel__cell moderator-panel__cell--to">
                            <span>
                                {{ item.uuid_to }}
                            </span>
                        </td>
                        <td class="moderator-panel__cell moderator-panel__cell--comment">
                            <span>
                                {{ item.description }}
                            </span>
                        </td>
                        <td class="moderator-panel__cell moderator-panel__cell--actions">
                            <CheckIcon v-if="!onlyHistory"
                                       @click="moderate('accept', item.id, item.uuid_to)"
                                       class="moderator-panel__action-btn moderator-panel__action-btn--accept" />
                            <div class="moderator-panel__cell--cancel primary-button"
                                 @click="moderate('return', (item as ICuratorActivityHistory).action_id, item.uuid_to, (item as ICuratorActivityHistory).valid)"
                                 v-else-if="(item as ICuratorActivityHistory).valid !== 2">
                                <span> Отменить</span>
                            </div>
                        </td>


                    </tr>
                </tbody>
                <tfoot class="moderator-panel__tfoot"></tfoot>
            </table>
        </div>
    </div>
</div>
<div class="admin-block-inner"
     v-else>
    {{ onlyHistory ? 'У вас нет истории отправленных баллов' : 'Нет активностей на подтверждение' }}
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
        CancelIcon,
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
            moderate: (type: string, id: number, uuidTo: number, valid?: number) => emit('moderate', type, id, uuidTo, valid),
        }
    }
})
</script>
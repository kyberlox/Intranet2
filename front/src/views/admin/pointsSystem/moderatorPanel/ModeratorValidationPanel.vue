<template>
    <div class="moderator-panel">
        <AdminSidebar v-if="isModer"
                      :needDefaultNav="false">
            <ModeratorSidebarSlot @areaClicked="changeActive"
                                  :moderatorsActivities="activitiesToConfirm" />
        </AdminSidebar>

        <div v-if="activitiesInTable?.length"
             class="moderator-panel__content">
            <div class="moderator-panel__list">
                <div class="moderator-panel__table-item"
                     v-for="item in activitiesInTable"
                     :key="item.id">
                    <table class="moderator-panel__table">
                        <thead class="moderator-panel__thead">
                            <tr class="moderator-panel__row">
                                <th class="moderator-panel__head">Дата</th>
                                <th class="moderator-panel__head">Параметр</th>
                                <th class="moderator-panel__head">От кого</th>
                                <th class="moderator-panel__head">Куда</th>
                                <th class="moderator-panel__head">Комментарий</th>
                                <th class="moderator-panel__head">
                                    <CancelIcon @click="moderate('cancel', item.id, item.uuid_to)"
                                                class="moderator-panel__action-btn moderator-panel__action-btn--cancel" />
                                </th>
                            </tr>
                        </thead>
                        <tbody class="moderator-panel__tbody">
                            <tr class="moderator-panel__row">
                                <td class="moderator-panel__cell moderator-panel__cell--date">
                                    {{ dateConvert(item.date_time, 'toStringType') }}
                                </td>
                                <td class="moderator-panel__cell moderator-panel__cell--parameter">
                                    {{ item.name }}
                                </td>
                                <td class="moderator-panel__cell moderator-panel__cell--from">
                                    {{ item.uuid_from }}
                                </td>
                                <td class="moderator-panel__cell moderator-panel__cell--to">
                                    {{ item.uuid_to }}
                                </td>
                                <td class="moderator-panel__cell moderator-panel__cell--comment">
                                    {{ item.description }}
                                </td>
                                <td class="moderator-panel__cell moderator-panel__cell--actions">
                                    <CheckIcon v-if="isModer"
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
    </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref, watch } from 'vue';
import CheckIcon from '@/assets/icons/common/Check.svg?component';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import Api from '@/utils/Api';
import { usePointsData } from '@/stores/PointsData';
import AdminSidebar from '@/views/admin/components/elementsListLayout/AdminSidebar.vue';
import { dateConvert } from '@/utils/dateConvert';
import ModeratorSidebarSlot from './ModeratorSidebarSlot.vue';

interface IActivityToConfirm {
    coast: number
    date_time: string
    description: string
    id: number
    name: number
    need_valid: boolean
    uuid_from: number
    uuid_to: number
}

export default defineComponent({
    props: {
        isModer: {
            type: Boolean,
            default: () => true
        }
    },
    components: {
        CheckIcon,
        CancelIcon,
        AdminSidebar,
        ModeratorSidebarSlot
    },
    setup(props) {
        const activeId = ref<number>();
        const activitiesToConfirm = computed(() => usePointsData().getActivitiesToConfirm);
        const activitiesInTable = ref<IActivityToConfirm[]>();

        const changeActive = (id: number) => {
            activeId.value = id;
        }

        const tableInit = () => {
            Api.get(`peer/confirmation/${activeId.value}`)
                .then((data) => {
                    activitiesInTable.value = data
                })
        }

        watch((activeId), () => {
            if (props.isModer && !activeId.value && activeId.value !== 0) return
            tableInit();
        }, { immediate: true, deep: true });



        const moderate = (type: 'accept' | 'cancel', rowId: number, uuidTo: number) => {
            Api.post(`/api/peer/${type == 'accept' ? 'do_valid' : 'do_not_valid'}`, { action_id: rowId, uuid_to: uuidTo })
                .then((data) => console.log(data))
                .finally(() => tableInit())
        }

        onMounted(() => {
            if (!props.isModer) {
                console.log('get');

                Api.get(`peer/confirmation/0`)
                    .then((data) => {
                        activitiesInTable.value = data
                    })
            }
        })

        return {
            activitiesToConfirm,
            activitiesInTable,
            activeId,
            dateConvert,
            changeActive,
            moderate
        }
    }
})

</script>
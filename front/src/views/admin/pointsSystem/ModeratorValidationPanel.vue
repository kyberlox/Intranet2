<template>
    <div class="moderator-panel__wrapper">
        <AdminSidebar :isModeratorArea="true"
                      :activeId="activeId"
                      @areaClicked="changeActive"
                      :moderatorsActivities="activitiesToConfirm" />
        <div v-if="activitiesInTable?.length"
             class="bottomTablePadding">
            <div class="forModeratorsTable">
                <div class="moderatorTableDiv"
                     v-for="item in activitiesInTable"
                     :key="item.id">
                    <table class="moderatorTable">
                        <thead>
                            <tr>
                                <th>Дата</th>
                                <th>Параметр</th>
                                <th>От кого</th>
                                <th>Куда</th>
                                <th>Комментарий</th>
                                <th>
                                    <CancelIcon @click="moderate('cancel', item.id, item.uuid_to)"
                                                class="moderator__button cancelBtn" />
                                </th>
                            </tr>
                        </thead>
                        <tbody id="moderatorBodyTable">
                            <tr class="1">
                                <td id="date">{{ dateConvert(item.date_time, 'toStringType') }}</td>
                                <td id="parameter">{{ item.name }}</td>
                                <td id="from">{{ item.uuid_from }}</td>
                                <td id="to">{{ item.uuid_to }}</td>
                                <td id="comm">{{ item.description }}</td>
                                <td>
                                    <CheckIcon @click="moderate('accept', item.id, item.uuid_to)"
                                               class="moderator__button acceptBtn" />
                                </td>
                            </tr>
                        </tbody>
                        <tfoot></tfoot>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import CheckIcon from '@/assets/icons/common/Check.svg?component';
import CancelIcon from '@/assets/icons/common/Cancel.svg?component';
import Api from '@/utils/Api';
import { usePointsData } from '@/stores/PointsData';
import AdminSidebar from '../components/elementsListLayout/AdminSidebar.vue';
import { dateConvert } from '@/utils/dateConvert';

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
    components: {
        CheckIcon,
        CancelIcon,
        AdminSidebar
    },
    setup(props) {
        const activeId = ref<number>();
        const activitiesToConfirm = computed(() => usePointsData().getActivitiesToConfirm);
        const activitiesInTable = ref<IActivityToConfirm[]>();
        const changeActive = (id: number) => {
            activeId.value = id;
        }

        watch((activeId), () => {
            if (!activeId.value && activeId.value !== 0) return
            tableInit();
        }, { immediate: true, deep: true });

        const tableInit = () => {
            Api.get(`peer/confirmation/${activeId.value}`)
                .then((data) => {
                    activitiesInTable.value = data
                })
        }

        const moderate = (type: 'accept' | 'cancel', rowId: number, uuidTo: number) => {
            Api.post(`/api/peer/${type == 'accept' ? 'do_valid' : 'do_not_valid'}`, { actionId: rowId, uuid_to: uuidTo })
                .then((data) => console.log(data))
                .finally(() => tableInit())
        }

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

<style lang="scss">
.forModeratorsTable {
    scrollbar-width: thin;
    background-color: #f8933c59;
    padding: 3%;
    border-radius: 46px;
    border: 1px solid #c4c4c4;
    max-height: 80vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
}


.moderatorTableDiv {
    display: flex;
    align-items: flex-end;
    justify-content: center;
}

.moderatorTable {
    border-collapse: collapse;
    width: 100%;
    margin: auto;
    border-radius: 16px;
    background-color: white;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.36);
    position: relative;
    transition: 0.2s;
}

.SuperAdminTable {
    border-collapse: collapse;
    width: 100%;
    margin: auto;
    border-radius: 16px;
    background-color: white;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.36);
    position: relative;
    transition: 0.2s;
}

.moderatorTable th,
.moderatorTable td {
    text-align: center;
    /* background-color: #ffe8c7ba; */
    color: black;
    border-bottom: 1px solid #ddd;
    padding: 18px;
}

.moderator__button {
    border-radius: 19px;
    background-color: #00cb20;
    color: white;
    // padding: 3px 10px;
    border: none;
    cursor: pointer;
    margin: 4px 0;
    border: 1px #00000042 solid;
    transition: all 0.3s;
    width: 40px;
    height: 35px;

}

.cancelBtn {
    background-color: #eb1212;

    &:hover {
        background-color: #eb1212a0;
    }
}

.acceptBtn {
    background-color: #00cb20;

    &:hover {
        background-color: #00cb1ea4;
    }
}

.moderator-panel__wrapper {
    display: flex;
    flex-direction: row;
}

.bottomTablePadding {
    flex-grow: 1;
}
</style>
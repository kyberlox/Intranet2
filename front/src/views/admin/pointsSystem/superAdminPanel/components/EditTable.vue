<template>
<div class="activity-edit">
    <div class="activity-edit__table-wrapper">
        <table class="activity-edit__table">
            <thead class="activity-edit__thead">
                <tr class="activity-edit__row activity-edit__row--head">
                    <th class="activity-edit__cell activity-edit__cell--head"
                        v-for="(head, index) in currentEntity?.keys"
                        :key="'head' + index">
                        {{ head }}
                    </th>
                </tr>
            </thead>
            <!--расскидываю типы табличек -->
            <div v-if="isLoading"
                 class="activity-edit__tbody">
                <div class="activity-edit__table__loader">
                    <Loader />
                </div>
            </div>
            <tbody v-else
                   class="activity-edit__tbody">
                <ActivityTable v-if="currentEntity?.name == 'activity'"
                               @editActivity="editActivity"
                               @deleteItem="deleteItem" />
                <ModeratorTable v-else-if="currentEntity?.name == 'moder'"
                                :moders="moders"
                                @deleteItem="deleteItem" />
                <CuratorTable v-else-if="currentEntity?.name == 'curator'"
                              :curators="curators"
                              @deleteItem="deleteItem" />
                <AdministratorTable v-else-if="currentEntity?.name == 'admin'"
                                    :admins="admins"
                                    @deleteItem="deleteItem" />
            </tbody>

            <tfoot class="activity-edit__tfoot"></tfoot>
        </table>
        <div class="activity-edit__add">
            <a class="activity-edit__add-btn primary-button"
               role="button"
               tabindex="0"
               @click="addNewModalVisible = true">
                Добавить
            </a>
        </div>
    </div>
    <AddNewEntinyModal v-if="addNewModalVisible"
                       :currentEntity="currentEntity?.name"
                       @addNew="addNewHandle"
                       @close="addNewModalVisible = false" />
</div>
</template>

<script lang="ts">
import { defineComponent, computed, ref, watch } from 'vue';
import CuratorTable from './tableEntities/CuratorTable.vue';
import ActivityTable from './tableEntities/ActivityTable.vue';
import ModeratorTable from './tableEntities/ModeratorTable.vue';
import AdministratorTable from './tableEntities/AdministratorTable.vue';
import Api from '@/utils/Api';
import AddNewEntinyModal from './AddNewEntinyModal.vue';
import type { INewActivityData } from '@/interfaces/IPutFetchData';
import type { ICurator, IPointsModer, IPointsAdmin } from '@/interfaces/IEntities';
import Loader from '@/components/layout/Loader.vue';
import { usePointsData } from '@/stores/PointsData';

export default defineComponent({
    name: 'EditTable',
    props: {
        activeId: {
            type: Number,
            required: true,
        },
    },
    components: {
        AddNewEntinyModal,
        CuratorTable,
        ActivityTable,
        ModeratorTable,
        AdministratorTable,
        Loader
    },
    setup(props) {
        const addNewModalVisible = ref(false);
        const curators = ref<ICurator[]>([]);
        const moders = ref<IPointsModer[]>([]);
        const admins = ref<IPointsAdmin[]>([]);
        const isLoading = ref(false);

        const entitiesHeaders: {
            id: number;
            keys: string[];
            name: 'activity' | 'curator' | 'moder' | 'admin';
        }[] = [{
            id: 1, keys: ['Параметр', 'Стоимость'], name: 'activity'
        },
        {
            id: 2, keys: ['Сотрудник', 'Активность'], name: 'curator'
        },
        {
            id: 3, keys: ['Сотрудник'], name: 'moder'
        },
        {
            id: 4, keys: ['Сотрудник'], name: 'admin'
        },
            ];

        const currentEntity = computed(() => entitiesHeaders.find((item) => item.id === props.activeId))

        const addNewHandle = (newEntity: INewActivityData) => {
            addNewModalVisible.value = false;
            isLoading.value = true;

            switch (currentEntity.value?.name) {
                case 'activity':
                    if (!newEntity) return;
                    Api.put('peer/new_activity', newEntity)
                        .then((data) => console.log(data))
                        .finally(() =>
                            setTimeout(() => {
                                reloadTable(('activity'))
                            }, 1000));
                    break;
                case 'curator':
                    Api.put(`peer/add_curator/${newEntity.uuid}/${newEntity.activity_id}`)
                        .then((data) => console.log(data))
                        .finally(() =>
                            setTimeout(() => {
                                reloadTable(('curator'))
                            }, 1000));
                    break;
                case 'moder':
                    Api.put(`peer/add_peer_moder/${newEntity.uuid}`)
                        .then((data) => console.log(data))
                        .finally(() =>
                            setTimeout(() => {
                                reloadTable(('moder'))
                            }, 1000));
                    break;
                case 'admin':
                    Api.put(`peer/add_peer_admin/${newEntity.uuid}`)
                        .then((data) => console.log(data))
                        .finally(() =>
                            setTimeout(() => {
                                reloadTable(('admin'))
                            }, 1000));
                    break;
                default:
                    break;
            }
        }

        const deleteItem = (type: 'activity' | 'admin' | 'moder' | 'curator', uid: number, activity_uid?: number) => {
            const prefixes = { activity: 'remove_activity', admin: 'delete_admin', moder: 'delete_peer_moder', curator: `delete_curator` }
            Api.delete(`peer/${prefixes[type]}/${uid}` + (activity_uid ? '/' + activity_uid : ''))
            setTimeout(() => {
                reloadTable((type))
            }, 1000);
        }

        const reloadTable = (table: 'curator' | 'moder' | 'admin' | 'activity') => {
            switch (table) {
                case 'activity':
                    Api.get('/peer/get_all_activities')
                        .then((data) => usePointsData().setAllActivities(data))
                        .finally(() => isLoading.value = false)
                case 'curator':
                    Api.get('peer/get_curators')
                        .then((data) => {
                            if (!data.status)
                                curators.value = data
                        })
                        .finally(() => isLoading.value = false)
                    break;
                case 'moder':
                    Api.get('peer/get_moders_list')
                        .then((data) => {
                            if (!data.status)
                                moders.value = data
                        })
                        .finally(() => isLoading.value = false)
                    break;
                case 'admin':
                    Api.get('peer/get_admins_list')
                        .then((data) => {
                            if (!data.status) admins.value = data
                        })
                        .finally(() => isLoading.value = false)
                    break;

                default:
                    break;
            }

        }
        watch((currentEntity), () => {
            if (!currentEntity.value?.name) return
            reloadTable(currentEntity.value?.name)
        }, { deep: true, immediate: true })

        const editActivity = (active: INewActivityData) => {
            Api.post('peer/edit_activity', active)
                .then((data) => console.log(data))
        }

        return {
            entitiesHeaders,
            addNewModalVisible,
            currentEntity,
            curators,
            admins,
            moders,
            isLoading,
            addNewHandle,
            deleteItem,
            editActivity
        };
    }
});

</script>
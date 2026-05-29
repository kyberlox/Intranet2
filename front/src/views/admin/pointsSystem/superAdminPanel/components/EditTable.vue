<template>
<div class="activity-edit">
    <div class="activity-edit__table-wrapper">
        <table class="activity-edit__table">
            <thead class="activity-edit__thead">
                <tr class="activity-edit__row activity-edit__row--head">
                    <th class="activity-edit__cell activity-edit__cell--head"
                        v-for="(head, index) in currentEntity?.keys"
                        :key="'head' + index">
                        <span> {{ head }}</span>
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
import { usePointsData } from '@/stores/pointsData';

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
            id: 1, keys: ['Параметр', 'Описание', 'Стоимость'], name: 'activity'
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

        const addNewHandle = async (newEntity: INewActivityData) => {
            isLoading.value = true;
            addNewModalVisible.value = false;
            const cases = [
                { name: 'activity', route: 'peer/new_activity' },
                { name: 'curator', route: `peer/add_curator/${newEntity.uuid}/${newEntity.activity_id}` },
                { name: 'moder', route: `peer/add_peer_moder/${newEntity.uuid}` },
                { name: 'admin', route: `peer/add_peer_admin/${newEntity.uuid}` }
            ]
            const name = cases.find(e => e.name == currentEntity?.value?.name)?.name
            const route = cases.find(e => e.name == currentEntity?.value?.name)?.route
            if (!route) return

            try {
                await Api.put(route, newEntity)
                setTimeout(() => {
                    reloadTable(name as "activity" | "curator" | "moder" | "admin")
                }, 1000);
            } catch (error) {
                console.error(error);
            }
        }

        const deleteItem = async (type: 'activity' | 'admin' | 'moder' | 'curator', uid: number, activity_uid?: number) => {
            const prefixes = { activity: 'remove_activity', admin: 'delete_admin', moder: 'delete_peer_moder', curator: `delete_curator` }
            try {
                await Api.delete(`peer/${prefixes[type]}/${uid}` + (activity_uid ? '/' + activity_uid : ''))
                setTimeout(() => {
                    reloadTable((type))
                }, 1000);
            } catch (error) {
                console.error(error)
            }
        }

        const reloadTable = async (table: 'curator' | 'moder' | 'admin' | 'activity') => {
            const cases = [
                { name: 'activity', route: '/peer/get_all_activities' },
                { name: 'curator', route: `peer/get_curators` },
                { name: 'moder', route: `peer/get_moders_list` },
                { name: 'admin', route: `peer/get_admins_list` }
            ]
            const route = cases.find(e => e.name == table)?.route
            if (!route) return
            try {
                const data = await Api.get(route)
                if (table == 'activity') usePointsData().setAllActivities(data)
                else if (table == 'curator') curators.value = data
                else if (table == 'moder') moders.value = data
                else if (table == 'admin') admins.value = data
            } finally {
                isLoading.value = false
            }
        }

        watch((currentEntity), () => {
            if (!currentEntity.value?.name) return
            reloadTable(currentEntity.value?.name)
        }, { deep: true, immediate: true })

        const editActivity = async (active: INewActivityData) => {
            try {
                await Api.post('peer/edit_activity', active)
            } catch (error) {
                console.error(error)
            }
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
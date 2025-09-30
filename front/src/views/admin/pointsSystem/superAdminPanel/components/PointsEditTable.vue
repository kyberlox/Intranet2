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
            <tbody class="activity-edit__tbody">
                <Component :is="currentEntity?.component"
                           @deleteItem="deleteItem" />
            </tbody>
            <tfoot class="activity-edit__tfoot"></tfoot>
        </table>
        <div class="activity-edit__add">
            <a class="activity-edit__add-btn primary-button"
               role="button"
               tabindex="0"
               @click="addNewModalVisible = true">Добавить </a>
        </div>
    </div>
    <AddNewEntinyModal v-if="addNewModalVisible"
                       :currentEntity="currentEntity?.name"
                       @addNew="addNewHandle"
                       @close="addNewModalVisible = false" />
</div>
</template>
<script lang="ts">
import { defineComponent, computed, ref } from 'vue';
import CuratorTable from './tableEntities/CuratorTable.vue';
import ActivityTable from './tableEntities/ActivityTable.vue';
import ModeratorTable from './tableEntities/ModeratorTable.vue';
import AdministratorTable from './tableEntities/AdministratorTable.vue';
import Api from '@/utils/Api';
import AddNewEntinyModal from './AddNewEntinyModal.vue';
import type { INewActivityData } from '@/interfaces/IPutFetchData';

export default defineComponent({
    name: 'EditTable',
    props: {
        activeId: {
            type: Number,
            required: true,
        },
    },
    components: {
        AddNewEntinyModal
    },
    setup(props) {
        const addNewModalVisible = ref(false);

        const entitiesHeaders = [{
            id: 1, keys: ['Параметр', 'Стоимость'], component: ActivityTable, name: 'activity'
        },
        {
            id: 2, keys: ['Сотрудник', 'Активность'], component: CuratorTable, name: 'curator'
        },
        {
            id: 3, keys: ['Сотрудник'], component: ModeratorTable, name: 'moder'
        },
        {
            id: 4, keys: ['Сотрудник'], component: AdministratorTable, name: 'admin'
        },
        ];

        const currentEntity = computed(() => entitiesHeaders.find((item) => item.id === props.activeId))

        const addNewHandle = (newEntity: INewActivityData) => {
            addNewModalVisible.value = false;
            switch (currentEntity.value?.name) {
                case 'activity':
                    if (!newEntity) return;
                    Api.put('peer/new_activity', newEntity)
                        .then((data) => console.log(data))
                    break;
                case 'curator':
                    Api.put(`peer/add_curator/${newEntity.id}/${newEntity.activity_id}`)
                        .then((data) => console.log(data))
                    break;
                case 'moder':
                    Api.put(`peer/add_peer_moder/${newEntity.id}`)
                        .then((data) => console.log(data))
                    break;
                case 'admin':
                    Api.put(`peer/add_peer_admin/${newEntity.id}`)
                        .then((data) => console.log(data))
                    break;

                default:
                    break;
            }
        }

        const deleteItem = (type: 'activity', id: number) => {
            const prefixes = { activity: 'remove_activity', admin: 'delete_admin', moder: 'delete_peer_moder' }
            Api.delete(`peer/${prefixes[type]}/${id}`)
        }

        return {
            entitiesHeaders,
            addNewModalVisible,
            currentEntity,
            addNewHandle,
            deleteItem,
        };
    }
});

</script>
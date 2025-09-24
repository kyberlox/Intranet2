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
                    <Component :is="currentEntity?.component" />
                </tbody>
                <tfoot class="activity-edit__tfoot"></tfoot>
            </table>
            <div class="activity-edit__add"><a class="activity-edit__add-btn primary-button"
                   role="button"
                   tabindex="0">Добавить </a></div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, computed } from 'vue';
import CuratorTable from './tableEntities/CuratorTable.vue';
import ActivityTable from './tableEntities/ActivityTable.vue';
import ModeratorTable from './tableEntities/ModeratorTable.vue';
import AdministratorTable from './tableEntities/AdministratorTable.vue';

export default defineComponent({

    name: 'EditTable',
    props: {
        activeId: {
            type: Number,
            required: true,
        },
    },
    setup(props) {
        const entitiesHeaders = [{
            id: 1, keys: ['Параметр', 'Стоимость'], component: ActivityTable
        },
        {
            id: 2, keys: ['Сотрудник', 'Активность'], component: CuratorTable
        },
        {
            id: 3, keys: ['Сотрудник'], component: ModeratorTable
        },
        {
            id: 4, keys: ['Сотрудник'], component: AdministratorTable
        },
        ];

        return {
            entitiesHeaders,
            currentEntity: computed(() => entitiesHeaders.find((item) => item.id === props.activeId)),
        };
    }
});

</script>
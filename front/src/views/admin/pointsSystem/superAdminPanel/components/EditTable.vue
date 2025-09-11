<template>
    <div class="activity-edit">
        <div class="activity-edit__table-wrapper">
            <table class="activity-edit__table">
                <thead class="activity-edit__thead">
                    <tr class="activity-edit__row activity-edit__row--head">
                        <th class="activity-edit__cell activity-edit__cell--head"
                            v-for="(head, index) in currentEntity?.keys"
                            :key="'head' + index">{{ head }}</th>
                    </tr>
                </thead>
                <tbody class="activity-edit__tbody">
                    <Component :is="currentEntity?.component" />
                </tbody>
            </table>

            <div class="activity-edit__add">
                <a class="activity-edit__add-link primary-button"
                   role="button"
                   tabindex="0">Добавить
                </a>
            </div>
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
    props: {
        activeId: {
            type: Number,
            required: true
        },
    },

    setup(props) {
        const entitiesHeaders = [
            { id: 1, keys: ['Параметр', 'Стоимость'], component: ActivityTable },
            { id: 2, keys: ['Сотрудник', 'Активность'], component: CuratorTable },
            { id: 3, keys: ['Сотрудник'], component: ModeratorTable },
            { id: 4, keys: ['Сотрудник'], component: AdministratorTable },
        ]

        return {
            entitiesHeaders,
            currentEntity: computed(() => entitiesHeaders.find((item) => item.id == props.activeId))
        }
    }
})
</script>

<style lang="scss">
.activity-edit {
    display: flex;
    flex-direction: column;
    width: 100%;

    &__table {
        border-collapse: collapse;
        width: 100%;
        margin: auto;
        border-radius: 16px;
        background-color: white;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.36);
        position: relative;
        transition: 0.2s;

        &-wrapper {
            max-width: 1200px;
            width: 100%;
            margin: auto;
        }
    }

    &__cell {
        text-align: center;
        /* background-color: #ffe8c7ba; */
        color: black;
        border-bottom: 1px solid #ddd;
        padding: 8px;
    }
}

.points-admin-panel {
    max-width: 1200px;
    width: 100%;
    margin: auto;
}

thead {
    border-bottom: 1px solid #ddd;
}

td {
    text-align: center;
    background-color: #e8e3df00;
    color: black;
    /* border-bottom: 1px solid #ddd; */
    padding: 8px;


    border-top: 1px solid #ddd;
    border-right: 1px solid #dddddd71;
}

.moderator__button {
    border-radius: 19px;
    background-color: #00cb20;
    color: white;
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

.activity-edit__input {
    // text-align: center;

    &:not(:focus) {
        border: 0;
        cursor: pointer;
    }
}

.activity-edit__field {
    &>svg {
        width: 20px;
    }
}

.activity-edit__add {
    margin-top: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.activity-edit__field {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 10px;

    &>input {
        flex-grow: 1;
    }
}
</style>
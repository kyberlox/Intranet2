<template>
<table class="point-info__table">
    <thead class="moderator-panel__thead">
        <tr class="moderator-panel__row">
            <th class="moderator-panel__head"
                v-if="allActivities?.length">
                <span>
                    Активность
                </span>
            </th>
            <th class="moderator-panel__head">
                <span>Баллы</span>
            </th>
        </tr>
    </thead>
    <tbody class="moderator-panel__tbody">
        <tr class="moderator-panel__row"
            v-for="activity in allActivities"
            :key="activity.id">
            <td v-if="activity.name"
                class="moderator-panel__cell moderator-panel__cell--date">
                <span>
                    {{ activity.name }}
                </span>
            </td>
            <td v-if="activity.coast"
                class="moderator-panel__cell moderator-panel__cell--parameter">
                <span>
                    {{ activity.coast }}
                </span>
            </td>
        </tr>
    </tbody>
    <tfoot class="moderator-panel__tfoot"></tfoot>
</table>
</template>

<script lang='ts'>
import { defineComponent } from 'vue';
import type { IActivitiesList } from '@/interfaces/IEntities';

export default defineComponent({
    components: {},
    props: {
        allActivities: {
            type: Array<IActivitiesList>
        }
    },
    setup() {
        return {

        }
    }
});
</script>
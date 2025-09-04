<template>
    <ul v-if="!editGroupMode"
        class="visibility-editor__area-users">
        <div v-for="userDep in formattedUsers"
             :key="userDep.depart"
             class="visibility-editor__area-user">
            <h1>{{ userDep.depart }}</h1>
            <li v-for="user in userDep.users"
                :key="user.id">
                <div class="visibility-editor__user-avatar">
                    <img v-if="user.photo"
                         :src="user.photo"
                         :alt="`${user.name} ${user.last_name}`"
                         class="visibility-editor__user-photo">
                </div>
                <div class="visibility-editor__user-fio">
                    {{ user.name + ' ' + user.last_name + ' ' + user.second_name }}
                </div>
            </li>
        </div>
    </ul>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { IFormattedUserGroup } from '../VisibilityAreaEditor.vue';
export default defineComponent({
    props: {
        editGroupMode: {
            type: Boolean
        },
        formattedUsers: {
            type: Array<IFormattedUserGroup>
        }
    },
    setup() {
        return {

        }
    }
})
</script>
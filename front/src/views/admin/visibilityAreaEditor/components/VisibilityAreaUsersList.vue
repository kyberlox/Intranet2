<template>
    <div v-if="!editGroupMode">
        <ul v-for="userDep in formattedUsers"
            :key="userDep.depart">
            <div class="mt20 visibility-editor__area-users__department-title">
                {{ userDep.depart }}
            </div>
            <div class="visibility-editor__area-users">
                <li v-for="user in userDep.users"
                    class="visibility-editor__area-user"
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
    </div>
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
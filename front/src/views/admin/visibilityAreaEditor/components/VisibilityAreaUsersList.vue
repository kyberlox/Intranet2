<template>
    <div v-if="!editGroupMode && formattedUsers?.length">
        <ul v-for="userDep in formattedUsers"
            :key="userDep.depart">
            <div class="mt20 visibility-editor__area-users__department-header">
                <div class="visibility-editor__area-users__department-title"
                     @click="showThisDep(userDep.depart_id)">
                    {{ userDep.depart }}
                </div>
                <CloseIcon @click="$emit('deleteArea', userDep.depart_id)" />
            </div>
            <div class="visibility-editor__area-users"
                 v-if="showingDeps.includes(userDep.depart_id)">
                <li v-for="user in userDep.users"
                    class="visibility-editor__area-user"
                    :class="{ 'visibility-editor__area-user--chosen': userChoices?.find((e) => e.id == user.id) }"
                    :key="user.id"
                    @click="$emit('pickUser', user)">
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
    <div class="mt20"
         v-else>
        Добавьте пользователей в текущую облась видимости
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import type { IFormattedUserGroup, IChoice } from '@/interfaces/IEntities';
import CloseIcon from '@/assets/icons/common/Cancel.svg?component';
export default defineComponent({
    props: {
        editGroupMode: {
            type: Boolean
        },
        formattedUsers: {
            type: Array<IFormattedUserGroup>
        },
        userChoices: {
            type: Array<IChoice>
        }
    },
    components: {
        CloseIcon
    },
    setup(props, { emit }) {
        const showingDeps = ref<number[]>([]);

        const showThisDep = (id: number) => {
            const target = showingDeps.value.findIndex((e) => e == id);
            if (target !== -1) {
                showingDeps.value.splice(target, 1)
            } else {
                showingDeps.value.push(id);
            }
        }

        return {
            showingDeps,
            showThisDep
        }
    }
})
</script>
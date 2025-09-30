<template>
<div class="visibility-editor__area-users"
     v-if="usersList">
    <li v-for="user in usersList"
        :key="user.id"
        class="visibility-editor__area-user"
        @click="pickUser(user)">
        <div class="visibility-editor__user-avatar">
            <img v-if="user.image"
                 :src="user.image"
                 :alt="`${user.name}`"
                 class="visibility-editor__user-photo">
        </div>
        <div class="visibility-editor__user-fio">
            {{ user.name }}
        </div>
    </li>
</div>
</template>

<script lang="ts">
import type { IUserSearch } from '@/interfaces/IEntities';
import { defineComponent, type PropType } from 'vue';

export default defineComponent({
    props: {
        usersList: {
            type: Array as PropType<IUserSearch[]>
        }
    },
    emits: ['pickUser'],
    setup(_, { emit }) {
        return {
            pickUser: (user: IUserSearch) => emit('pickUser', user)
        }
    }
})
</script>
<template>
<UsersSearchList v-if="users"
                 :usersList="formatUsers(users)"
                 :needDeleteButton="true" />
</template>

<script lang="ts">
import UsersSearchList from "@/components/tools/common/UsersSearchList.vue";
import { defineComponent, type PropType } from "vue";
import type { IUserSearch } from "@/interfaces/IEntities";

export interface IUserList {
    fio: string
    id: number
    name: string
    photo_file_url?: string
    position: string
}

export default defineComponent({
    components: {
        UsersSearchList
    },
    props: {
        users: {
            type: Array as PropType<IUserList[]>
        }
    },
    setup() {
        const formatUsers = (usersArr: IUserList[]) => {
            if (!usersArr.length) return;
            const formatUsers: IUserSearch[] = [];
            usersArr.map((e) => {
                formatUsers.push({ name: e.fio ? e.fio : e.name, user_position: e.position, image: e.photo_file_url, id: e.id })
            })
            return formatUsers
        }

        return {
            formatUsers
        }
    }
})
</script>
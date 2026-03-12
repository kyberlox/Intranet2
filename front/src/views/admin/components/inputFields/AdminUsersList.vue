<template>
<UsersSearchList v-if="users"
                 :usersList="formatUsers(users)"
                 :needDeleteButton="true" />
</template>

<script lang="ts">
import UsersSearchList from "@/components/tools/common/UsersSearchList.vue";
import { defineComponent, type PropType } from "vue";
import type { IUserSearch } from "@/interfaces/IEntities";
import type { IAreaDepartment } from "./AdminEditAreaSearch.vue";

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
            type: Array as PropType<IUserList[] | IAreaDepartment[]>
        },
        type: {
            type: String,
            default: "users"
        }
    },
    setup(props) {
        const formatUsers = (usersArr: IUserList[] | IAreaDepartment[]) => {
            if (!usersArr.length) return;
            const formattedUsers: IUserSearch[] = [];
            if (props.type == 'users') {
                (usersArr as IUserList[]).map((e) => {
                    formattedUsers.push({ name: e.fio ? e.fio : e.name, user_position: e.position, image: e.photo_file_url, id: e.id })
                })
            }
            else if (props.type == 'departments') {
                usersArr.map((e) => {
                    formattedUsers.push({ name: e.name, user_position: '', image: '', id: e.id })
                })
            }
            return formattedUsers
        }

        return {
            formatUsers
        }
    }
})
</script>
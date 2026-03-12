<template>
<div class="visibility-editor__area-users"
     v-if="searchList">
    <li v-for="element in formatElements(searchList)"
        :key="element.id"
        class="visibility-editor__area-user"
        @click="pickElement(element)">
        <div v-if="element.image"
             class="visibility-editor__user-avatar">
            <img :src="element.image"
                 :alt="`${element.name}`"
                 class="visibility-editor__user-photo">
        </div>
        <div class="visibility-editor__user-fio">
            {{ element.name }}
        </div>
        <div v-if="needDeleteButton"
             class="visibility-editor__user__remove-btn"
             @click="$emit('remove', element.id)">
            <Cancel />
        </div>
    </li>
</div>
</template>

<script lang="ts">
import type { IUserSearch } from '@/interfaces/IEntities';
import { defineComponent, type PropType } from 'vue';
import Cancel from '@/assets/icons/common/Cancel.svg?component';
import type { IAreaDepartment } from '@/views/admin/components/inputFields/AdminEditAreaSearch.vue';

export interface IUserList {
    fio: string
    id: number
    name: string
    photo_file_url?: string
    image?: string
    position: string
}

export default defineComponent({
    props: {
        searchList: {
            type: Array as PropType<IUserSearch[] | IAreaDepartment[]>
        },
        needDeleteButton: {
            type: Boolean,
            default: () => false
        },
        type: {
            type: String,
            default: "users"
        }

    },
    components: {
        Cancel
    },
    emits: ['pick', 'remove'],
    setup(props, { emit }) {

        const formatElements = (elements: IUserList[] | IAreaDepartment[]) => {
            if (!elements.length) return;
            const formattedUsers: IUserSearch[] = [];
            if (props.type == 'users') {
                (elements as IUserList[]).map((e) => {
                    formattedUsers.push({ name: e.fio ? e.fio : e.name, user_position: e.position, image: e.photo_file_url || e.image, id: e.id })
                })
            }
            else if (props.type == 'departments') {
                elements.map((e) => {
                    formattedUsers.push({ name: e.name, user_position: '', image: '', id: e.id })
                })
            }
            console.log(formattedUsers);

            return formattedUsers
        }
        return {
            formatElements,
            pickElement: (user: IUserSearch) => emit('pick', user)
        }
    }
})
</script>
<template>
    <div v-if="!editGroupMode && formattedUsers?.length">
        <ul v-for="userDep in formattedUsers"
            :key="userDep.depart">
            <div v-if="depNeedToBeShown(userDep)">
                <div class="mt20 visibility-editor__area-users__department-header">
                    <div class="visibility-editor__area-users__department-title"
                         @click="showThisDep(userDep.depart_id)">
                        {{ userDep.depart }}
                    </div>
                    <CloseIcon @click="$emit('deleteDep', userDep.depart_id)" />
                </div>
                <div class="visibility-editor__area-users"
                     v-if="showingDeps.includes(userDep.depart_id) || showAllDepsUsers">
                    <li v-for="user in userDep.users"
                        class="visibility-editor__area-user"
                        :class="{ 'visibility-editor__area-user--chosen': userChoices?.find((e) => e.id == user.id) }"
                        :key="user.id"
                        @click="$emit('pickUser', user)">
                        <div class="visibility-editor__user-avatar">
                            <img v-if="user.image"
                                 :src="user.image"
                                 :alt="`${user.name} ${user.last_name}`"
                                 class="visibility-editor__user-photo">
                        </div>
                        <div class="visibility-editor__user-fio">
                            {{ user.name }}
                        </div>
                    </li>
                </div>
            </div>
        </ul>
    </div>
    <div class="mt20"
         v-else>
        {{ activeArea ? 'Добавьте пользователей в облась видимости' : 'Создайте и выберите область видимости' }}
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
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
        },
        fioFilter: {
            type: String
        },
        depFilter: {
            type: String
        },
        activeArea: {
            type: Number
        }
    },
    components: {
        CloseIcon
    },
    emits: ['deleteDep', 'pickUser'],
    setup(props, { emit }) {
        const showAllDepsUsers = computed(() => {
            return (props.depFilter || props.fioFilter) ? true : false
        })
        const showingDeps = ref<number[]>([]);

        const showThisDep = (id: number) => {
            const target = showingDeps.value.findIndex((e) => e == id);
            if (target !== -1) {
                showingDeps.value.splice(target, 1)
            } else {
                showingDeps.value.push(id);
            }
        }

        const depNeedToBeShown = (userDep: IFormattedUserGroup) => {
            if (props.depFilter) {
                return userDep.depart.toLocaleLowerCase().includes(props.depFilter.toLocaleLowerCase())
            }
            else if (props.fioFilter) {
                return userDep.users.find((e) => e.name.includes(String(props.fioFilter)))
            }
            else
                return true;
        }

        return {
            showAllDepsUsers,
            showingDeps,
            showThisDep,
            depNeedToBeShown
        }
    }
})
</script>
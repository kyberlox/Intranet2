<template>
<ul class="visibility-editor__area-departments mt20"
    v-if="!userDisplayMode">
    <li class="visibility-editor__area-department"
        v-for="dep in departmentsToShow"
        :key="dep.id">
        <PlusIcon @click.stop.prevent="changeVisibility(dep.id)"
                  v-if="!showingDeps.includes(dep.id)" />
        <MinusIcon @click.stop.prevent="changeVisibility(dep.id)"
                   v-else />
        <div class="visibility-editor__area-department__info">
            <span @click.stop.prevent="changeVisibility(dep.id)">
                {{ dep.name }}
            </span>
            <ul class="visibility-editor__area-department__info__users">
                <li v-show="showingDeps.includes(dep.id)"
                    class="visibility-editor__area-user italic"
                    @click="fixUserChoice('allDep', dep.id)">
                    Добавить весь отдел с подотделами
                </li>
                <li v-show="showingDeps.includes(dep.id)"
                    class="visibility-editor__area-user italic"
                    @click="fixUserChoice('onlyDep', dep.id)">
                    Добавить отдел без подотделов
                </li>
                <li v-show="showingDeps.includes(dep.id)"
                    class="visibility-editor__area-user visibility-editor__area-user--inDep"
                    :class="{ 'visibility-editor__area-user--chosen': choices?.find((e) => e.id == user.id) }"
                    v-for="user in dep.users"
                    :key="user.id"
                    @click="fixUserChoice('user', dep.id, user.id)">
                    <img v-if="user.image"
                         class="visibility-editor__area-user-avatar"
                         :src="user.image" />
                    {{ user.name }}
                </li>
            </ul>
            <VisibilityAreaEditorTree v-if="showingDeps.includes(dep.id)"
                                      @fixUserChoice="(type, depId, userId) =>
                                        fixUserChoice(type, depId, userId)"
                                      :choices="choices"
                                      :departments="dep.departments" />
        </div>
    </li>
</ul>
<ul class="visibility-editor__area-users--userMode"
    v-else>
    <li class="visibility-editor__area-user visibility-editor__area-user--inDep visibility-editor__area-user--userMode"
        :class="{ 'visibility-editor__area-user--chosen': choices?.find((e) => e.id == user.id) }"
        v-for="user in filteredUsers"
        :key="user.id"
        @click="$emit('fixUserChoice', 'user', user.dep_id, user.id)">
        <img v-if="user.image"
             class="visibility-editor__area-user-avatar"
             :src="user.image" />
        {{ user.name }}
    </li>
</ul>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref, watch } from 'vue';
import PlusIcon from '@/assets/icons/admin/PlusIcon.svg?component'
import MinusIcon from '@/assets/icons/admin/MinusIcon.svg?component'
import type { IDepartment, IChoice, IUserSearch } from '@/interfaces/IEntities';

export default defineComponent({
    name: 'VisibilityAreaEditorTree',
    props: {
        departments: {
            type: Array as PropType<IDepartment[]>
        },
        filteredDepartments: {
            type: Array as PropType<IDepartment[]>
        },
        filteredUsers: {
            type: Array as PropType<IUserSearch[]>
        },
        choices: {
            type: Array<IChoice>
        }
    },
    emits: ['fixUserChoice'],
    components: {
        PlusIcon,
        MinusIcon
    },
    setup(props, { emit }) {
        const showingDeps = ref<number[]>([]);
        const userDisplayMode = ref(false);
        const departmentsToShow = ref();

        watch((props), () => {
            if (props.filteredUsers?.length) {
                userDisplayMode.value = true
            } else userDisplayMode.value = false;

            if (props.filteredDepartments?.length) {
                departmentsToShow.value = props.filteredDepartments;
            }
            else departmentsToShow.value = props.departments;
        }, { immediate: true, deep: true })

        const changeVisibility = (id: number) => {
            const target = showingDeps.value.findIndex((e) => e == id);
            if (target == -1) {
                showingDeps.value.push(id);
            }
            else showingDeps.value.splice(target, 1);
        }

        return {
            userDisplayMode,
            departmentsToShow,
            showingDeps,
            fixUserChoice: (type: string, depId: number, userId?: number) => emit('fixUserChoice', type, depId, userId),
            changeVisibility
        }
    }
})
</script>
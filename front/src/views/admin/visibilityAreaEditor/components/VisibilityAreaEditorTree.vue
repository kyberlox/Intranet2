<template>
    <ul class="visibility-editor__area-departments">
        <li class="visibility-editor__area-department"
            v-for="dep in departments"
            :key="dep.id">
            <PlusIcon @click.stop.prevent="changeVisibility(dep.id)"
                      v-if="!showingDeps.includes(dep.id)" />
            <MinusIcon @click.stop.prevent="changeVisibility(dep.id)"
                       v-else />
            <div class="visibility-editor__area-department__info">
                <span @click.stop.prevent="changeVisibility(dep.id)">{{ dep.name }}</span>
                <ul class="visibility-editor__area-department__info__users">
                    <li v-show="showingDeps.includes(dep.id)"
                        class="visibility-editor__area-user italic"
                        @click="$emit('fixUserChoice', 'onlyDep', dep.id)">
                        Добавить весь отдел
                    </li>
                    <li v-show="showingDeps.includes(dep.id)"
                        class="visibility-editor__area-user italic"
                        @click="$emit('fixUserChoice', 'allDep', dep.id)">
                        Добавить весь отдел с подотделами
                    </li>
                    <li v-show="showingDeps.includes(dep.id)"
                        class="visibility-editor__area-user visibility-editor__area-user--inDep"
                        v-for="user in dep.users"
                        :key="user.user_id"
                        @click="$emit('fixUserChoice', 'user', dep.id, user.user_id)">
                        <img v-if="user.photo"
                             class="visibility-editor__area-user-avatar"
                             :src="user.photo" />
                        {{ user.user_fio }}
                    </li>
                </ul>
                <VisibilityAreaEditorTree v-if="showingDeps.includes(dep.id)"
                                          @fixUserChoice="(type, depId, userId) =>
                                            $emit('fixUserChoice', type, depId, userId)"
                                          :departments="dep.departments" />
            </div>
        </li>
    </ul>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from 'vue';
import PlusIcon from '@/assets/icons/admin/PlusIcon.svg?component'
import MinusIcon from '@/assets/icons/admin/MinusIcon.svg?component'
import type { IDepartment, IUserSearch } from '../VisibilityAreaEditor.vue';

export default defineComponent({
    name: 'VisibilityAreaEditorTree',
    props: {
        departments: {
            type: Array as PropType<IDepartment[]>
        },
        choices: {

        }
    },
    emits: ['fixUserChoice'],
    components: {
        PlusIcon,
        MinusIcon
    },
    setup(props, { emit }) {
        const showingDeps = ref<number[]>([]);

        const changeVisibility = (id: number) => {
            const target = showingDeps.value.findIndex((e) => e == id);
            if (target == -1) {
                showingDeps.value.push(id);
            }
            else showingDeps.value.splice(target, 1);
        }


        return {
            showingDeps,
            changeVisibility
        }
    }
})
</script>
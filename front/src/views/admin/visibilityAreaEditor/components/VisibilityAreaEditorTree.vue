<template>
    <ul class="visibility-editor__area-departments">
        <li class="visibility-editor__area-department"
            @click="changeVisibility(dep.id)"
            v-for="dep in departments"
            :key="dep.id">
            <PlusIcon v-if="!showingDeps.includes(dep.id)" />
            <MinusIcon v-else />
            <div class="visibility-editor__area-department__info">
                <span>{{ dep.name }}</span>
                <ul class="visibility-editor__area-department__info__users"
                    :class="{ 'hidden': !showingDeps.includes(dep.id) }">
                    <li class="visibility-editor__area-user visibility-editor__area-user--inDep"
                        v-for="user in dep.users"
                        :key="user.user_id">
                        {{ user.user_fio }}
                    </li>
                </ul>
                <VisibilityAreaEditorTree :departments="dep.departments" />
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
        }
    },
    components: {
        PlusIcon,
        MinusIcon
    },
    setup() {
        const showingDeps = ref<number[]>([]);

        const changeVisibility = (id: number) => {
            const target = showingDeps.value.findIndex((e) => e == id);
            if (target == -1) {
                showingDeps.value.push(id)
            }
            else showingDeps.value.splice(target, 1)
        }

        return {
            showingDeps,
            changeVisibility
        }
    }
})
</script>
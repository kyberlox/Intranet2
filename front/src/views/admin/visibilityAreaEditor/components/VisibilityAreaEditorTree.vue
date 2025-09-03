<template>
    <ul class="visibility-editor__area-departments">
        <li class="visibility-editor__area-department"
            v-for="dep in departments"
            :key="dep.id">
            <PlusIcon />
            <div class="visibility-editor__area-department__info">
                <span>{{ dep.name }}</span>
                <ul class="visibility-editor__area-department__info__users ">
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
        const showThisDeps = ref<number[]>([])
        const changeVisibility = (id: number) => {
            showThisDeps.value.find((e) => e == id)
        }
        return {

        }
    }
})
</script>
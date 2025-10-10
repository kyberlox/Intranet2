<template>
<AdminEditUserSearch />

</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import AdminEditUserSearch from "./AdminEditUserSearch.vue";
import MinusIcon from '@/assets/icons/admin/MinusIcon.svg?component';
import PlusIcon from '@/assets/icons/admin/PlusIcon.svg?component';

export default defineComponent({
    components: {
        AdminEditUserSearch,
        PlusIcon,
        MinusIcon
    },
    setup() {
        const users = ref<string[]>([]);

        const addNewReportRow = () => {
            users.value.push()
        }

        const RemoveReportRow = () => {
            users.value.splice(-2, 2);
        }

        return {
addNewReportRow,
RemoveReportRow,
        }
    }
})
</script>

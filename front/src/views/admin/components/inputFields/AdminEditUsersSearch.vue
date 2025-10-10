<template>
<AdminEditUserSearch />
<div class="admin-element__reportage-group__add-button__wrapper ">
    <div @click="addNewReportRow"
         class="admin-element__reportage-group__add-button primary-button">
        <PlusIcon />
    </div>
    <div @click="RemoveReportRow"
         class="admin-element__reportage-group__add-button primary-button">
        <MinusIcon />
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import AdminEditUserSearch from "./AdminEditUserSearch.vue";

export default defineComponent({
    components: {
        AdminEditUserSearch
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

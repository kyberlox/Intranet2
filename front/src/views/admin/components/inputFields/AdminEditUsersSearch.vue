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
import { defineComponent } from "vue";
import AdminEditUserSearch from "./AdminEditUserSearch.vue";

export default defineComponent({
    components: {
        AdminEditUserSearch
    },
    setup() {
        const users: Ref<{}[]> = ref([]);
        const addNewReportRow = ''
        const RemoveReportRow = ''
        const addNewReportRow = () => {
            formattedReportages.value.push({ name: 'Название', value: '' }, { name: 'Ссылка', value: '' })
        }

        const RemoveReportRow = () => {
            formattedReportages.value.splice(-2, 2);
        }

        return {

        }
    }
})
</script>
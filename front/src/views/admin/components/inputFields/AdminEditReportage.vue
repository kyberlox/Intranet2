<template>
<p class="admin-element-inner__field-title fs-l">Репортажи</p>
<div class="admin-element__reportage-group__wrapper mt20">
    <transition-group tag="div"
                      name="slide-down"
                      class="admin-element__reportage-list">
        <AdminEditInput v-for="(reportage, index) in formattedReportages"
                        :key="index + 'reportage'"
                        :item="reportage"
                        @pick="(newVal: string) => changeReport(index, newVal)" />
    </transition-group>
</div>
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
import { defineComponent, onMounted, ref, type Ref, type PropType } from 'vue';
import AdminEditInput from './AdminEditInput.vue';
import type { IReportage } from '@/interfaces/IEntities';
import PlusIcon from '@/assets/icons/admin/PlusIcon.svg?component'
import MinusIcon from '@/assets/icons/admin/MinusIcon.svg?component'
export default defineComponent({
    props: {
        item: {
            type: Array as PropType<IReportage[]>
        },
    },
    components: {
        AdminEditInput,
        PlusIcon,
        MinusIcon
    },
    emits: ['pick'],
    setup(props, { emit }) {
        const reportages = ref(props.item);
        const itemsCount = ref(1);
        const formattedReportages: Ref<{ name: string, value: string }[]> = ref([]);

        onMounted(() => {
            if (!reportages.value) return;
            reportages.value.map((e) => {
                formattedReportages.value.push({ name: 'Название', value: e.name }, { name: 'Ссылка', value: e.link })
            })
        })

        const addNewReportRow = () => {
            formattedReportages.value.push({ name: 'Название', value: '' }, { name: 'Ссылка', value: '' })
        }

        const RemoveReportRow = () => {
            formattedReportages.value.splice(-2, 2);
        }

        const changeReport = (index: number, newVal: string) => {
            formattedReportages.value[index].value = newVal;
            emitInPrevFormat();
        }

        const emitInPrevFormat = () => {
            const prevFormat = [];
            const chunkSize = 2;
            for (let i = 0; i < formattedReportages.value.length; i += chunkSize) {
                const chunk = formattedReportages.value.slice(i, i + chunkSize);
                prevFormat.push({ name: chunk[0].value, link: chunk[1].value })
            }
            emit('pick', prevFormat)
        }

        return {
            itemsCount,
            formattedReportages,
            addNewReportRow,
            changeReport,
            RemoveReportRow
        }
    }
})
</script>

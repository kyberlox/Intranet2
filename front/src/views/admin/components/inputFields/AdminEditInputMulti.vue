<template>
<p class="admin-element-inner__field-title fs-l">
    {{ title }}
</p>
<div class="admin-element__reportage-group__wrapper">
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
import type { IBXFileType } from '@/interfaces/IEntities';
import type { IReportage } from '@/interfaces/IEntities';
import PlusIcon from '@/assets/icons/admin/PlusIcon.svg?component'
import MinusIcon from '@/assets/icons/admin/MinusIcon.svg?component'
export default defineComponent({
    props: {
        item: {
            type: Array as PropType<IReportage[] | IBXFileType[]>
        },
        title: {
            type: String,
            default: () => 'Репортажи'
        },
        articleId: {
            type: Number
        }
    },
    components: {
        AdminEditInput,
        PlusIcon,
        MinusIcon
    },
    emits: ['pick', 'saveEmbed'],
    setup(props, { emit }) {
        const reportages = ref(props.item);
        const isReportages = Boolean(props.title == 'Репортажи');

        const formattedReportages: Ref<{ name?: string, value: string }[]> = ref([]);

        onMounted(() => {
            if (reportages.value?.length) {
                reportages.value.map((e) => {
                    if (isReportages) {
                        formattedReportages.value.push(
                            { name: 'Название', value: String('name' in e ? e.name : e.original_name) },
                            { name: 'Ссылка', value: String('link' in e ? e.link : e.file_url) })
                    } else {
                        formattedReportages.value.push(
                            { name: 'Ссылка', value: String('link' in e ? e.link : e.file_url) })
                    }
                })
            }

        })

        const addNewReportRow = () => {
            if (isReportages) {
                formattedReportages.value.push({ name: 'Название', value: '' }, { name: 'Ссылка', value: '' })
            } else {
                formattedReportages.value.push({ name: 'Ссылка', value: '' })
            }
        }

        const RemoveReportRow = () => {
            if (isReportages) {
                formattedReportages.value.splice(-2, 2);
            }
            else {
                formattedReportages.value.splice(-1, 1);
            }
            emitInPrevFormat()
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
                if (isReportages) {
                    prevFormat.push({ name: chunk[0].value, link: chunk[1].value })
                }
                else {
                    formattedReportages.value.forEach((e) => prevFormat.push(e.value))
                }
            }
            if (isReportages) {
                emit('pick', prevFormat)
            }
            else
                emit('saveEmbed', prevFormat)
        }

        return {
            formattedReportages,
            addNewReportRow,
            changeReport,
            RemoveReportRow
        }
    }
})
</script>

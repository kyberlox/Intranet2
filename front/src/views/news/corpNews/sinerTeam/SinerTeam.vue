<template>
  <div>
    <h1 class="page__title mt20">Организационное Развитие</h1>

    <SinerTable
      :rows="tableRows"
      :columns="tableColumns"
      :loading="loading"
      @row-click="handleRowClick"
    >
      <template #column-implementer="{ value }">
        <div class="person-cell">
          <img
            v-if="value && value[0]?.photo_file_url"
            :src="value[0].photo_file_url"
            :alt="value[0]?.fio || 'Фото'"
            class="person-avatar"
          />
          <span>{{ value?.[0]?.fio || "" }}</span>
        </div>
      </template>

      <template #column-integrator="{ value }">
        <div class="person-cell">
          <img
            v-if="value && value[0]?.photo_file_url"
            :src="value[0].photo_file_url"
            :alt="value[0]?.fio || 'Фото'"
            class="person-avatar"
          />
          <span>{{ value?.[0]?.fio || "Работа без интегратора" }}</span>
        </div>
      </template>

      <template #column-status="{ value }">
        <span
          :class="[
            'status-badge',
            value === 'Запущен' ? 'status-active' : 'status-closed',
          ]"
        >
          {{ value }}
        </span>
      </template>

      <template #column-date_status="{ value }">
        {{ formatDate(value as string) }}
      </template>

      <template #column-note_status="{ value }">
        <div class="note-cell">
          {{ value || "—" }}
        </div>
      </template>
    </SinerTable>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from "vue";
import type { ColumnDefinition, TableRow } from "@/components/layout/SinerTable.vue";
import type { ISinerTableData } from "@/interfaces/entities/ISinerteam";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import SinerTable from "@/components/layout/SinerTable.vue";

export default defineComponent({
  name: "SinerTeam",

  components: {
    SinerTable,
  },

  setup() {
    const loading = ref(false);
    const tableData = ref<ISinerTableData[]>([]);

    const tableRows = computed<TableRow[]>(() => {
      if (!tableData.value || !Array.isArray(tableData.value)) {
        return [];
      }

      return tableData.value.map((item) => ({
        id: item.id,
        name: item.name,
        ...item.indirect_data,
      }));
    });

    const tableColumns = computed<ColumnDefinition[]>(() => [
      {
        key: "sinerteam_number",
        label: "Номер синертима",
        field: "sinerteam_number",
        sortable: true,
      },
      {
        key: "sinerteam_name",
        label: "Название синертима",
        field: "name",
        sortable: true,
      },
      {
        key: "implementer",
        label: "Имплементер",
        field: "implementer",
        sortable: true,
      },
      {
        key: "integrator",
        label: "Интегратор",
        field: "integrator",
        sortable: true,
      },
      {
        key: "status",
        label: "Статус",
        field: "sinerteam_status",
        sortable: true,
      },
      {
        key: "date_status",
        label: "Дата статуса",
        field: "date_status",
        sortable: true,
      },
      {
        key: "note_status",
        label: "Комментарий",
        field: "note_status",
      },
    ]);

    const formatDate = (date: string): string => {
      if (!date) return "—";
      try {
        const [datePart, timePart] = date.split(" ");
        const [day, month, year] = datePart.split(".");
        const [hours, minutes, seconds] = timePart.split(":");

        return new Date(
          Number(year),
          Number(month) - 1,
          Number(day),
          Number(hours),
          Number(minutes),
          Number(seconds)
        ).toLocaleDateString();
      } catch (error) {
        console.error("Date formatting error:", error);
        return "—";
      }
    };

    const handleRowClick = ({ row, index }: { row: TableRow; index: number }) => {
      console.log("Clicked row:", row, index);
    };

    const loadData = async () => {
      loading.value = true;
      try {
        const data = await Api.get(`article/find_by/${sectionTips["синертим"]}`);
        console.log(data);
        tableData.value = Array.isArray(data) ? data : [];
      } catch {
        tableData.value = [];
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadData();
    });

    return {
      tableRows,
      tableColumns,
      loading,
      formatDate,
      handleRowClick,
    };
  },
});
</script>

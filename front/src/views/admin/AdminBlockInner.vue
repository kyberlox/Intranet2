<template>
  <div class="admin-panel__editor-table mt20">
    <SearchAndButtons />
    <div class="table-container">
      <table class="events-table">
        <thead>
          <tr>
            <th v-for="(item, index) in sampleEvent[0]"
                :key="index">{{ item.name }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(event, index) in sampleEvent"
              :key="index">
            <td v-for="(item, index) in event"
                @click="router.push({ name: 'adminElementInner', params: { id: route.params.id, elementId: event.id.value } })"
                :key="index">
              {{ item.value }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import SearchAndButtons from '@/components/admin/SearchAndButtons.vue';
import Api from '@/utils/Api';
import { useRouter, useRoute } from 'vue-router';
interface Event {
  id: number;
  active: boolean;
  content_text: string;
  date_publiction: string;
  date_creation: string;
  preview_text: string;
  name: string;
  indirect_data: {
    id: number;
    IBLOCK_id: number;
    NAME: string;
    CREATED_BY: string;
    BP_PUBLISHED: string;
    CODE: string | null;
    DATE_CREATE: string;
    ACTIVE_FROM_X: string;
    ACTIVE_FROM: string;
    PROPERTY_290: string[];
    PROPERTY_291: Array<{ TEXT: string }>;
  };
}

export default defineComponent({
  components: {
    SearchAndButtons,
  },
  setup() {
    const events = ref<Event[]>([]);
    const router = useRouter();
    const route = useRoute();

    const sampleEvent = [
      {
        id: {
          name: 'id',
          value: '1',
        },
        name: {
          name: 'Название',
          value: 'Testzapis'
        },
        activno: {
          name: 'Активно',
          value: 'Нет'
        },
        date_publiction: {
          name: 'Дата публикации',
          value: '02-02-2002'
        },
        date_creation: {
          name: 'Дата создания',
          value: '02-02-2002'
        },
        inner_text: {
          name: 'Текст записи',
          value: 'вставить '
        },
        author: {
          name: 'Автор',
          value: 'тест-пример автора'
        },
        author1: {
          name: 'Автор1',
          value: 'тест-пример автора'
        },
        author2: {
          name: 'Автор2',
          value: 'тест-пример автора'
        },
      },
      {
        id: {
          name: 'id',
          value: '1',
        },
        name: {
          name: 'Название',
          value: 'Testzapis'
        },
        activno: {
          name: 'Активно',
          value: 'Нет'
        },
        date_publiction: {
          name: 'Дата публикации',
          value: '02-02-2002'
        },
        date_creation: {
          name: 'Дата создания',
          value: '02-02-2002'
        },
        inner_text: {
          name: 'Текст записи',
          value: 'вставить '
        },
        author: {
          name: 'Автор',
          value: 'тест-пример автора'
        },
        author1: {
          name: 'Автор1',
          value: 'тест-пример автора'
        },
        author2: {
          name: 'Автор2',
          value: 'тест-пример автора'
        }
      },
    ]

    const formatDate = (dateString: string) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('ru-RU');
    };

    const truncateHtml = (html: string, maxLength = 100) => {
      if (!html) return '';
      const textOnly = html.replace(/<[^>]*>/g, '');
      if (textOnly.length <= maxLength) return textOnly;
      return textOnly.substring(0, maxLength) + '...';
    };

    return {
      events,
      formatDate,
      truncateHtml,
      sampleEvent,
      router,
      route
    };
  }
});
</script>

<style>
.table-container {
  width: 100%;
  overflow-x: auto;
  margin-bottom: 20px;
}

.events-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1200px;
  /* Ensure table is wider than container to enable scrolling */
}

.events-table th,
.events-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.events-table th {
  background-color: #f2f2f2;
  position: sticky;
  top: 0;
}

.events-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.events-table tr:hover {
  background-color: #f1f1f1;
}

.truncate {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Add responsive styles */
@media screen and (max-width: 768px) {
  .table-container {
    margin: 0 -15px;
    /* Negative margin to extend container */
  }
}
</style>

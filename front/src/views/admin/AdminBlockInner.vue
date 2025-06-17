<template>
  <div class="admin-panel__editor-table mt20">
    <SearchAndButtons />
    <div class="table-container">
      <table class="events-table">
        <thead>
          <tr>
            <th v-for="(item, index) in sampleEvent[0]"
                :key="index">{{ item.name }}</th>
            <th class="actions-column">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(event, index) in sampleEvent"
              :key="index">
            <td v-for="(item, index) in event"
                @click="router.push({ name: 'adminElementInner', params: { id: route.params.id, elementId: event.id.value } })"
                :key="index">
              {{ item.value }}
            </td>
            <td class="actions-cell">
              <div class="action-buttons">
                <button class="icon-button edit-button"
                        @click.stop="editItem()"
                        title="Редактировать">
                  <EditIcon />
                </button>
                <button class="icon-button delete-button"
                        @click.stop="deleteItem()"
                        title="Удалить">
                  <CloseIcon />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import SearchAndButtons from '@/components/admin/SearchAndButtons.vue';
import Api from '@/utils/Api';
import { useRouter, useRoute } from 'vue-router';
import EditIcon from '@/assets/icons/admin/EditIcon.svg?component'
import CloseIcon from '@/assets/icons/admin/CloseIcon.svg?component'

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
    EditIcon,
    SearchAndButtons,
    CloseIcon
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
      route,
      editItem: () => console.log('edit'),
      deleteItem: () => console.log('delete'),
    };
  }
});
</script>

<style scoped lang="scss">
.admin-panel__editor-table {
  border-radius: 16px;
  padding: 24px;
  /* box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); */
  min-height: 100dvh;
}

.table-container {
  width: 100%;
  overflow-x: auto;
  margin-bottom: 20px;
  border-radius: 12px;
  background: white;
  box-shadow: 1px -1px 40px rgb(0 0 0 / 22%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.events-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 1200px;
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.events-table th,
.events-table td {
  padding: 16px 20px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.events-table th {
  background: white;
  position: sticky;
  top: 0;
  font-weight: 600;
  color: #334155;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #e2e8f0;
  z-index: 10;
}

.events-table th:first-child {
  border-top-left-radius: 12px;
}

.events-table th:last-child {
  border-top-right-radius: 12px;
}

.events-table tbody tr {
  transition: all 0.3s ease;
  cursor: pointer;
}

.events-table tbody tr:hover {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.events-table tbody tr:nth-child(even) {
  background-color: #fafbfc;
}

.events-table tbody tr:nth-child(even):hover {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.events-table td {
  color: #475569;
  font-weight: 500;
  position: relative;
}

.events-table tbody tr:hover td::before {
  transform: scaleY(1);
}

.truncate {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.actions-column {
  width: 140px;
  text-align: center;
}

.actions-cell {
  text-align: center;
  cursor: default;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.icon-button {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.icon-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.icon-button:hover::before {
  transform: translateX(0);
}

.edit-button {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.edit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
}

.edit-button:active {
  transform: translateY(0);
}

.delete-button {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
}

.delete-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4);
}

.delete-button:active {
  transform: translateY(0);
}

.events-table tbody tr {
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive styles */
@media screen and (max-width: 768px) {
  .admin-panel__editor-table {
    padding: 16px;
    margin: 0 -15px;
    border-radius: 0;
  }

  .table-container {
    border-radius: 8px;
    margin: 0;
  }

  .events-table {
    border-radius: 8px;
  }

  .events-table th,
  .events-table td {
    padding: 12px 8px;
    font-size: 14px;
  }

  .action-buttons {
    flex-direction: column;
    gap: 8px;
  }

  .icon-button {
    width: 32px;
    height: 32px;
  }

  .actions-column {
    width: 80px;
  }
}

@media screen and (max-width: 480px) {

  .events-table th,
  .events-table td {
    padding: 8px 4px;
    font-size: 12px;
  }

  .icon-button {
    width: 28px;
    height: 28px;
  }
}
</style>

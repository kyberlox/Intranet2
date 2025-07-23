<template>
  <div class="admin-page__wrapper">
    <AdminSidebar />
    <div class="admin-block-inner">
      <div class="admin-block-inner__header">
        <h1 class="admin-block-inner__title">{{ currentSection?.name || 'Редактирование раздела' }}</h1>
        <p class="admin-block-inner__description">
          Управляйте содержимым раздела
        </p>
      </div>

      <div class="admin-block-inner__content">
        <div class="admin-block-inner__toolbar">
          <div class="admin-block-inner__toolbar-left">
            <button class="admin-block-inner__btn admin-block-inner__btn--primary">
              <svg width="16"
                   height="16"
                   viewBox="0 0 24 24"
                   fill="currentColor">
                <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
              </svg>
              Добавить элемент
            </button>
          </div>
          <div class="admin-block-inner__toolbar-right">
            <div class="admin-block-inner__search">
              <svg width="16"
                   height="16"
                   viewBox="0 0 24 24"
                   fill="currentColor"
                   class="admin-block-inner__search-icon">
                <path
                      d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
              </svg>
              <input type="text"
                     placeholder="Поиск..."
                     class="admin-block-inner__search-input"
                     v-model="searchQuery">
            </div>
          </div>
        </div>

        <div class="admin-block-inner__main">
          <div class="admin-block-inner__cards">
            <div v-for="item in filteredItems"
                 :key="item.id"
                 class="admin-block-inner__card">
              <div class="admin-block-inner__card-header">
                <h3 class="admin-block-inner__card-title">{{ item.title }}</h3>
                <div class="admin-block-inner__card-actions">
                  <button class="admin-block-inner__card-btn"
                          title="Редактировать">
                    <svg width="16"
                         height="16"
                         viewBox="0 0 24 24"
                         fill="currentColor">
                      <path
                            d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
                    </svg>
                  </button>
                  <button class="admin-block-inner__card-btn admin-block-inner__card-btn--danger"
                          title="Удалить">
                    <svg width="16"
                         height="16"
                         viewBox="0 0 24 24"
                         fill="currentColor">
                      <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
                    </svg>
                  </button>
                </div>
              </div>
              <div class="admin-block-inner__card-content">
                <p class="admin-block-inner__card-description">{{ item.description }}</p>
                <div class="admin-block-inner__card-meta">
                  <span class="admin-block-inner__card-status"
                        :class="`admin-block-inner__card-status--${item.status}`">
                    {{ getStatusText(item.status) }}
                  </span>
                  <span class="admin-block-inner__card-date">{{ formatDate(item.updatedAt) }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="filteredItems.length === 0"
               class="admin-block-inner__empty">
            <svg width="64"
                 height="64"
                 viewBox="0 0 24 24"
                 fill="currentColor"
                 class="admin-block-inner__empty-icon">
              <path
                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
            </svg>
            <h3 class="admin-block-inner__empty-title">Элементы не найдены</h3>
            <p class="admin-block-inner__empty-description">
              В этом разделе пока нет элементов или они не соответствуют критериям поиска
            </p>
            <button class="admin-block-inner__btn admin-block-inner__btn--primary">
              Создать первый элемент
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import Api from '@/utils/Api';
import AdminSidebar from './AdminSidebar.vue';

interface SectionItem {
  id: number;
  title: string;
  description: string;
  status: boolean;
  updatedAt: string;
}

export default defineComponent({
  components: {
    AdminSidebar
  },
  setup() {
    const route = useRoute();
    const currentSection = ref();
    const items = ref<SectionItem[]>([]);
    const searchQuery = ref('');

    const filteredItems = computed(() => {
      if (!searchQuery.value) return items.value;
      return items.value.filter(item =>
        item.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        item.description.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    const getStatusText = (status: boolean) => {
      return status ? 'Активен' : 'В архиве'
    };

    const formatDate = (dateString: string) => {
      return new Date(dateString).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
    };

    onMounted(() => {
      const sectionId = route.params.id;

      // Загрузка информации о разделе
      Api.get(`section/${sectionId}`)
        .then((res) => {
          currentSection.value = res;
        });

      // Загрузка элементов раздела
      Api.get(`section/${sectionId}/items`)
        .then((res) => {
          items.value = res;
        })
        .catch(() => {
          // Заглушка для демонстрации
          items.value = [
            {
              id: 1,
              title: 'Пример элемента 1',
              description: 'Описание первого элемента раздела',
              status: true,
              updatedAt: '2024-01-15T10:30:00Z'
            }
          ];
        });
    });

    return {
      currentSection,
      items,
      searchQuery,
      filteredItems,
      getStatusText,
      formatDate
    };
  }
});
</script>

<style scoped>
.admin-page__wrapper {
  display: flex;
  min-height: 100vh;
  height: 100%;
  background-color: #f8f9fa;
}

.admin-block-inner {
  flex: 1;
  padding: 24px;
  margin-left: 0;
  overflow-x: auto;
}

.admin-block-inner__header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e9ecef;
}

.admin-block-inner__title {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  color: #212529;
  line-height: 1.2;
}

.admin-block-inner__description {
  margin: 0;
  font-size: 16px;
  color: #6c757d;
  line-height: 1.5;
}

.admin-block-inner__content {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.admin-block-inner__toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.admin-block-inner__toolbar-left {
  display: flex;
  gap: 12px;
}

.admin-block-inner__toolbar-right {
  display: flex;
  align-items: center;
}

.admin-block-inner__btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.admin-block-inner__btn--primary {
  background: #007bff;
  color: white;
}

.admin-block-inner__btn--primary:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

.admin-block-inner__btn--secondary {
  background: #6c757d;
  color: white;
}

.admin-block-inner__btn--secondary:hover {
  background: #545b62;
  transform: translateY(-1px);
}

.admin-block-inner__search {
  position: relative;
  display: flex;
  align-items: center;
}

.admin-block-inner__search-icon {
  position: absolute;
  left: 12px;
  color: #6c757d;
  pointer-events: none;
}

.admin-block-inner__search-input {
  padding: 10px 12px 10px 40px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 14px;
  width: 250px;
  transition: border-color 0.2s ease;
}

.admin-block-inner__search-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.admin-block-inner__main {
  padding: 24px;
}

.admin-block-inner__cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, 1fr);
  gap: 20px;
}

.admin-block-inner__card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s ease;
}

.admin-block-inner__card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.admin-block-inner__card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.admin-block-inner__card-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #212529;
  line-height: 1.3;
}

.admin-block-inner__card-actions {
  display: flex;
  gap: 8px;
}

.admin-block-inner__card-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  background: #f8f9fa;
  color: #6c757d;
  cursor: pointer;
  transition: all 0.2s ease;
}

.admin-block-inner__card-btn:hover {
  background: #e9ecef;
  color: #495057;
}

.admin-block-inner__card-btn--danger:hover {
  background: #dc3545;
  color: white;
}

.admin-block-inner__card-content {
  margin-top: 12px;
}

.admin-block-inner__card-description {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: #6c757d;
  line-height: 1.5;
}

.admin-block-inner__card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.admin-block-inner__card-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.admin-block-inner__card-status--true {
  background: #d4edda;
  color: #155724;
}

.admin-block-inner__card-status--false {
  background: #f8d7da;
  color: #721c24;
}

.admin-block-inner__card-date {
  font-size: 12px;
  color: #adb5bd;
}

.admin-block-inner__empty {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
}

.admin-block-inner__empty-icon {
  margin-bottom: 20px;
  opacity: 0.5;
}

.admin-block-inner__empty-title {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 600;
  color: #495057;
}

.admin-block-inner__empty-description {
  margin: 0 0 24px 0;
  font-size: 16px;
  line-height: 1.5;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

/* Responsive */
@media (max-width: 1024px) {
  .admin-page__wrapper {
    flex-direction: column;
  }

  .admin-block-inner {
    margin-left: 0;
  }
}

@media (max-width: 768px) {
  .admin-block-inner {
    padding: 16px;
  }

  .admin-block-inner__toolbar {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .admin-block-inner__toolbar-left,
  .admin-block-inner__toolbar-right {
    justify-content: center;
  }

  .admin-block-inner__search-input {
    width: 100%;
  }

  .admin-block-inner__cards {
    grid-template-columns: 1fr;
  }

  .admin-block-inner__card-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>
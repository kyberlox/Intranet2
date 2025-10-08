<template>
<div class="admin-block__page__wrapper">
  <AdminSidebar :needDefaultNav="true" />
  <div class="admin-block-inner"
       v-if="items">
    <div class="admin-block-inner__content">
      <div class="admin-block-inner__toolbar">
        <div class="admin-block-inner__toolbar-left">
          <RouterLink :to="{ name: 'adminElementInnerAdd', params: { id: sectionId } }"
                      class="admin-block-inner__btn admin-block-inner__btn--primary">
            <svg width="16"
                 height="16"
                 viewBox="0 0 24 24"
                 fill="currentColor">
              <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
            </svg>
            Добавить элемент
          </RouterLink>
        </div>
        <div class="admin-block-inner__toolbar-right">
          <div class="admin-block-inner__search">
            <SearchIcon class="admin-block-inner__search-icon" />
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
            <RouterLink :to="{ name: 'adminElementInnerEdit', params: { elementId: item.id } }"
                        class="admin-block-inner__card__wrapper">
              <div v-if="item.preview_file_url"
                   class="admin-block-inner__card__side-img"
                   :class="{ 'bg-contain': sectionId == '41' }"
                   v-lazy-load="item.preview_file_url"></div>
              <div class="flex-grow">
                <div class="admin-block-inner__card-header">
                  <h3 class="admin-block-inner__card-title">{{ item.name }}</h3>
                  <div class="admin-block-inner__card-actions">
                    <button class="admin-block-inner__card-btn"
                            title="Редактировать">
                      <EditIcon />
                    </button>
                    <button @click.stop.prevent="removeItem(item.id)"
                            class="admin-block-inner__card-btn admin-block-inner__card-btn--danger"
                            title="Удалить">
                      <RemoveIcon />
                    </button>
                  </div>
                </div>
                <div class="admin-block-inner__card-content">
                  <p v-if="item.content_text"
                     class="admin-block-inner__card-description"
                     v-html="item.content_text"></p>
                  <div class="admin-block-inner__card-meta">
                    <span class="admin-block-inner__card-status"
                          :class="`admin-block-inner__card-status--${item.active}`">
                      {{ getStatusText(Boolean(item.active)) }}
                    </span>
                    <div class="d-flex flex-column mt20">
                      <span v-if="item.indirect_data?.TITLE"
                            class="admin-block-inner__card-date">
                        {{ item.indirect_data?.TITLE }}
                      </span>
                      <span v-if="item.date_publiction"
                            class="admin-block-inner__card-date">
                        {{ useDateFormat(item.date_publiction, 'DD.MM.YYYY') }}
                      </span>
                      <span v-else-if="item.date_creation"
                            class="admin-block-inner__card-date">
                        {{ useDateFormat(item.date_creation, 'DD.MM.YYYY') }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </RouterLink>
          </div>
        </div>

        <div v-if="filteredItems.length === 0"
             class="admin-block-inner__empty">
          <div v-if="!isLoading">
            <h3 class="admin-block-inner__empty-title">Элементы не найдены</h3>
            <p class="admin-block-inner__empty-description">
              В этом разделе пока нет элементов или они не соответствуют критериям поиска
            </p>
          </div>
          <div class="admin-block-inner__loader"
               v-else>
            <Loader />
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import Api from '@/utils/Api';
import AdminSidebar from '@/views/admin/components/AdminSidebar.vue';
import Loader from '@/components/layout/Loader.vue';
import { useDateFormat } from '@vueuse/core';
import SearchIcon from "@/assets/icons/layout/SearchIcon.svg?component";
import EditIcon from "@/assets/icons/admin/EditIcon.svg?component"
import RemoveIcon from "@/assets/icons/admin/RemoveIcon.svg?component"

import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import { handleApiResponse } from '@/utils/ApiResponseCheck';
import { handleApiError } from '@/utils/ApiResponseCheck';

interface SectionItem {
  id: number;
  preview_file_url?: string,
  name?: string,
  content_text: string,
  active?: string,
  date_publiction?: string,
  date_creation?: string,
  indirect_data?: {
    TITLE?: string
  }
}

export default defineComponent({
  components: {
    AdminSidebar,
    Loader,
    SearchIcon,
    EditIcon,
    RemoveIcon,
  },
  props: {
    id: {
      type: String
    }
  },
  setup(props) {
    const route = useRoute();
    const items = ref<SectionItem[]>([]);
    const searchQuery = ref('');
    const isLoading = ref(false);
    const sectionId = ref();

    const toastInstance = useToast();
    const toast = useToastCompose(toastInstance);

    const filteredItems = computed(() => {
      if (!searchQuery.value) return items.value;
      return items.value.filter(item =>
        item.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        item.content_text?.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    const getStatusText = (status: boolean) => {
      return status ? 'Активен' : 'В архиве'
    };

    const itemsInit = () => {
      items.value.length = 0;
      isLoading.value = true;
      sectionId.value = route.params.id;
      Api.get(`/editor/section_rendering/${sectionId.value}`)
        .then((data) => items.value = data)
        .finally(() => isLoading.value = false)
    }

    watch((props), () => {
      itemsInit();
    }, { immediate: true, deep: true });

    const removeItem = (id: number) => {
      Api.delete(`editor/del/${id}`)
        .then((data) => {
          handleApiResponse(data, toast, 'trySupportError', 'adminDeleteSuccess')
        })
        .catch((error) => {
          handleApiError(error, toast)
        })
        .finally(() => {
          itemsInit();
        })
    }

    return {
      items,
      searchQuery,
      filteredItems,
      isLoading,
      sectionId,
      getStatusText,
      removeItem,
      useDateFormat
    };
  }
});
</script>
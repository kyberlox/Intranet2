<template>
  <div class="admin-element-inner">
    <Transition :name="previewFullWidth ? 'layout-change' : 'layout-change-toLeft'"
                mode="out-in">
      <div class="admin-element-inner__wrapper admin-element-inner__wrapper--mt20"
           :class="{ 'admin-element-inner__wrapper--preview-full-width': previewFullWidth }"
           :key="previewFullWidth ? 'fullwidth' : 'normal'">
        <div class="admin-element-inner__editor"
             :class="[
              { 'admin-element-inner__editor--preview-full-width': previewFullWidth },
              { 'admin-element-inner__editor--no-preview': activeType == 'noPreview' }
            ]">
          <div v-for="(item, index) in newElementSkeleton"
               class="admin-element-inner__field"
               :class="{ 'admin-element-inner__field--preview-full-width': previewFullWidth }"
               :key="index">

            <AdminComponentDatePicker v-if="inputComponentChecker(item) == 'datePicker'"
                                      :item="item"
                                      @pick="(value: string) => handleEmitValueChange(item, value)" />

            <AdminComponentSelect v-else-if="inputComponentChecker(item) == 'select'"
                                  :item="item"
                                  @pick="(value: string) => handleEmitValueChange(item, value)" />


            <AdminComponentTextarea v-else-if="inputComponentChecker(item) == 'textArea'"
                                    :item="item"
                                    @pick="(value: string) => handleEmitValueChange(item, value)" />


            <AdminComponentInput v-else-if="inputComponentChecker(item) == 'input'"
                                 :item="item"
                                 @pick="(value: string) => handleEmitValueChange(item, value)" />


            <AdminComponentImagePicker v-else-if="inputComponentChecker(item) == 'image'"
                                       :item="item" />

            <AdminComponentDocPicker v-else-if="inputComponentChecker(item) == 'docs'"
                                     :item="item" />

            <div v-else-if="inputComponentChecker(item) == 'auto'"
                 class="admin-element-inner__field-content">
              <p v-if="item.name"
                 class="admin-element-inner__field-title">{{ item.name }}</p>
              <p v-if="item.value"
                 class="admin-element-inner__field-value">{{ item.value }}</p>
            </div>

          </div>
        </div>

        <div class="admin-element-inner__preview"
             :class="{ 'admin-element-inner__preview--full-width': previewFullWidth }">
          <Transition name="layout-change"
                      mode="out-in">
            <LayoutTop v-if="previewFullWidth"
                       class="admin-element-inner__layout-toggle admin-element-inner__layout-toggle--zoom"
                       @click="previewFullWidth = !previewFullWidth" />
            <LayoutLeft v-else
                        class="admin-element-inner__layout-toggle admin-element-inner__layout-toggle--zoom"
                        @click="previewFullWidth = !previewFullWidth" />
          </Transition>

          <PostInner v-if="newData && activeType == 'news'"
                     class="admin-element-inner__preview-content"
                     :previewElement="newData"
                     :type="'adminPreview'" />
          <Interview v-if="activeType == 'interview'"
                     class="admin-element-inner__preview-content"
                     :interviewInner="currentItem" />
          <CertainBlog v-if="activeType == 'blogs'"
                       class="admin-element-inner__preview-content"
                       :interviewInner="currentItem"
                       :id="String(15238)"
                       :authorId="String(157)" />
        </div>
      </div>
    </Transition>

    <div class="admin-element-inner__actions">
      <button @click="applyNewData"
              class="admin-element-inner__action-button admin-element-inner__action-button--save">
        <span class="admin-element-inner__action-text">Сохранить</span>
      </button>
      <RouterLink :to="{ name: 'admin' }"
                  class="admin-element-inner__action-button admin-element-inner__action-button--cancel">
        <span class="admin-element-inner__action-text">Отменить</span>
      </RouterLink>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import Api from '@/utils/Api';

import LayoutLeft from "@/assets/icons/admin/LayoutLeft.svg?component";
import LayoutTop from "@/assets/icons/admin/LayoutTop.svg?component";

import PostInner from '@/components/tools/common/PostInner.vue';
import Interview from '@/views/about/ourPeople/components/Interview.vue';
import CertainBlog from '../about/blogs/CertainBlog.vue';

import AdminComponentSelect from './components/AdminComponentSelect.vue';
import AdminComponentTextarea from './components/AdminComponentTextarea.vue';
import AdminComponentDatePicker from './components/AdminComponentDatePicker.vue';
import AdminComponentInput from './components/AdminComponentInput.vue';
import AdminComponentImagePicker from './components/AdminComponentImagePicker.vue';
import AdminComponentDocPicker from './components/AdminComponentDocPicker.vue';

import { type IPostInner } from '@/components/tools/common/PostInner.vue';
import type { IAdminListItem } from '@/interfaces/entities/IAdmin';
import { chooseImgPlug } from '@/utils/chooseImgPlug';

type AdminElementValue = string | number | string[] | boolean | undefined | Array<{ link: string; name: string }>;

export default defineComponent({
  components: {
    LayoutLeft,
    LayoutTop,
    PostInner,
    Interview,
    CertainBlog,
    AdminComponentTextarea,
    AdminComponentSelect,
    AdminComponentDatePicker,
    AdminComponentInput,
    AdminComponentImagePicker,
    AdminComponentDocPicker
  },
  props: {
    id: {
      type: String
    },
    elementId: {
      type: String
    },
    type: {
      type: String,
      default: 'edit'
    }
  },

  setup(props) {
    const newElementSkeleton: Ref<IAdminListItem[]> = ref([]);
    const events = ref<Event[]>([]);
    const router = useRouter();
    const previewFullWidth = ref(false);
    const activeType = ref('news');

    const currentItem: Ref<IPostInner> = ref({ id: 0 });
    const newData: Ref<IPostInner> = ref({ id: 0, images: [chooseImgPlug()] });

    const inputComponentChecker = (item: IAdminListItem) => {
      if (item.disabled) return;
      switch (true) {
        case item.data_type == 'str' && String(item.field)?.includes('date'):
          return 'datePicker'
        case item.data_type == 'str' && 'values' in item:
          return 'select'
        case item.data_type == 'str' && item.field !== 'name' && !String(item.field).includes('url'):
          return 'textArea'
        case item.data_type == 'str':
          return 'input'
        case item.data_type == 'image':
          return 'image'
        case item.data_type == 'doc':
          return 'docs'
        default:
          return 'auto';
      }
    }

    onMounted(() => {
      if (props.type == 'new') {
        Api.get(`/editor/add/${props.id}`)
          .then((data) => { newElementSkeleton.value = data.fields })
      }
    })

    const applyNewData = () => {
      Api.post('/editor/add', newData.value)
    }

    const handleEmitValueChange = (item: IAdminListItem, value: AdminElementValue) => {
      if (item.field) {
        newData.value = {
          ...newData.value,
          [item.field]: value
        };
      }
    };
    return {
      events,
      router,
      currentItem,
      previewFullWidth,
      activeType,
      newElementSkeleton,
      inputComponentChecker,
      newData,
      applyNewData,
      handleEmitValueChange
    };
  }
});
</script>

<style lang="scss" scoped>
.admin-element-inner {
  &__type-buttons {
    margin-top: 20px;
  }

  &__type-button {
    margin-right: 10px;
    padding: 8px 16px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      background-color: #f5f5f5;
    }
  }

  &__wrapper {
    display: flex;
    flex-direction: row;
    gap: 40px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;

    &--mt20 {
      margin-top: 20px;
    }

    &--preview-full-width {
      flex-direction: column-reverse;
    }
  }

  &__editor {
    display: flex;
    flex-direction: column;
    gap: 15px;
    min-width: 33%;

    &--preview-full-width {
      align-items: center;
      align-content: center;
      border-top: 1px solid gainsboro;
      padding-top: 40px;
    }

    &--no-preview {
      width: 100%;
      align-items: center;
    }
  }

  &__field {
    min-width: 250px;
    max-width: 500px;
    width: 100%;

    &:empty {
      display: none;
    }

    &--preview-full-width {
      max-width: 50%;
    }
  }

  &__field-content {
    &--no-transition {
      transition: none !important;
    }
  }

  &__field-title {
    margin: 0;
    padding: 0;
    font-weight: 500;
    margin-bottom: 8px;
  }

  &__field-value {
    padding: 8px 12px;
    background-color: #f9f9f9;
    border: 1px solid #eee;
    border-radius: 4px;
    min-height: 40px;
    display: flex;
    align-items: center;
    margin: 0;
  }

  &__input,
  &__select {
    width: 100%;
    height: 40px;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    box-sizing: border-box;

    &:disabled {
      background-color: #f5f5f5;
      cursor: not-allowed;
    }
  }

  &__select {
    appearance: none;
    background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23131313%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    background-size: 10px;
    padding-right: 30px;
  }

  &__select-option {
    // Стили для опций селекта
  }

  &__date-picker {
    transition: none !important;
  }

  &__text-editor {
    width: 100%;
  }

  &__gallery {
    display: grid;
    gap: 5px;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }

  &__gallery-card {
    width: 100%;
    object-fit: contain;
    aspect-ratio: 16 / 9;
    position: relative;
  }

  &__gallery-image {
    width: 100%;
    height: 100%;
    position: absolute;
    border-radius: 5px;
  }

  &__gallery-actions {
    position: absolute;
    top: 5px;
    right: 5px;
    display: flex;
    gap: 5px;
  }

  &__gallery-button {
    color: white;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      transform: scale(1.1);
    }

    &--view {
      background-color: #1890ff;
      color: white;
    }

    &--delete {
      background-color: #ff4d4f;
      color: white;
    }
  }

  &__img-uploader {
    margin-top: 10px;
  }

  &__documents {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
  }

  &__document-link {
    color: blue;
    transition: 0.1s;
    margin-bottom: 5px;

    &:hover {
      color: orange;
    }
  }

  &__file-uploader {
    margin-top: 10px;
  }

  &__preview {
    overflow: hidden;
    flex-grow: 1;
    height: fit-content;
    position: sticky;
    top: 100px;

    &--full-width {
      position: relative;
      top: auto;
    }
  }

  &__layout-toggle {
    position: absolute;
    width: 25px;
    right: 0;
    transition: 0.2s;
    cursor: pointer;

    &--zoom {
      &:hover {
        color: var(--emk-brand-color);
      }
    }
  }

  &__actions {
    margin: auto;
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
  }

  &__action-button {
    background-color: var(--emk-brand-color);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    min-width: 120px;

    &:hover {
      transform: translateY(-1px);
    }

    &:active {
      transform: translateY(0);
    }

    &:focus {
      outline: none;
      box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.3);
    }

    &--save {
      &:hover {
        background: #6ed110;
      }
    }

    &--cancel {
      background-color: #f5f5f5;
      color: #333;
      border: 1px solid #ddd;

      &:hover {
        background-color: #e8e8e8;
      }
    }
  }
}

:deep(.p-editor-container) {
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 100%;
}



.layout-change-enter-active,
.layout-change-leave-active,
.layout-change-toLeft-enter-active,
.layout-change-toLeft-leave-active {
  transition: all 0.2s ease;
}

.layout-change-enter-from,
.layout-change-leave-to {
  opacity: 0.7;
  transform: translateX(-30px);
}

.layout-change-toLeft-enter-from,
.layout-change-toLeft-leave-to {
  opacity: 0.7;
  transform: translateX(30px);
}
</style>

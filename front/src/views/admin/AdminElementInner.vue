<template>
  <div class="admin-element-inner">
    <div class="admin-element-inner__wrapper mt20"
         :class="{ 'admin-element-inner__wrapper--preview-full-width': previewFullWidth || isMobileScreen }">
      <div v-if="newElementSkeleton.length"
           class="admin-element-inner__editor"
           :class="[
            { 'admin-element-inner__editor--preview-full-width': previewFullWidth || isMobileScreen },
            { 'admin-element-inner__editor--no-preview': activeType == 'noPreview' }
          ]">
        <div v-for="(item, index) in newElementSkeleton"
             class="admin-element-inner__field"
             :key="index">

          <Component :is="inputComponentChecker(item)"
                     :item="item"
                     @pick="(value: string) => handleEmitValueChange(item, value)" />
        </div>

        <div class="admin-element-inner__field">
          <AdminComponentInput v-if="newElementFiles.videos_embed"
                               :item="{ name: 'Видео с источников', field: 'videos_embed', value: newElementFiles?.videos_embed[0]?.original_name ?? undefined }"
                               @pick="(value: string) => handleEmitValueChange({ name: 'Видео с источников', field: 'videos_embed' }, value)" />
        </div>
        <AdminUploadingSection :newFileData="newFileData"
                               :newElementFiles="newElementFiles"
                               :newData="newData"
                               @reloadData="reloadElementData(true)"
                               @handleUpload="handleUpload" />
      </div>

      <div v-else
           class="admin-element-inner__editor">
        <Loader class="admin-element-inner__editor__loader loader" />
      </div>

      <AdminPostPreview :previewFullWidth="previewFullWidth"
                        :isMobileScreen="isMobileScreen"
                        :newFileData="newFileData"
                        :newData="newData"
                        :activeType="activeType"
                        :currentItem="currentItem"
                        @changePreviewWidth="previewFullWidth = !previewFullWidth" />

    </div>

    <div class="admin-element-inner__actions">
      <button @click="applyNewData"
              :disabled="buttonIsDisabled"
              class="admin-element-inner__action-button admin-element-inner__action-button--save">
        <span class="admin-element-inner__action-text">Сохранить</span>
      </button>
      <RouterLink :to="{ name: 'adminBlockInner', params: { id: id } }"
                  class="admin-element-inner__action-button admin-element-inner__action-button--cancel">
        <span class="admin-element-inner__action-text">Назад</span>
      </RouterLink>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, type Ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import Api from '@/utils/Api';

import AdminComponentSelect from './components/AdminComponentSelect.vue';
import AdminComponentTextarea from './components/AdminComponentTextarea.vue';
import AdminComponentDatePicker from './components/AdminComponentDatePicker.vue';
import AdminComponentInput from './components/AdminComponentInput.vue';

import { type IPostInner } from '@/components/tools/common/PostInner.vue';
import type { IAdminListItem, newFileData } from '@/interfaces/entities/IAdmin';
import { chooseImgPlug } from '@/utils/chooseImgPlug';
import Loader from '@/components/layout/Loader.vue';
import { handleApiError, handleApiResponse } from '@/utils/ApiResponseCheck';
import FileUploader from './components/FileUploader.vue';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import { type IBXFileType } from "@/interfaces/IEntities";
import { screenCheck } from '@/utils/screenCheck';
import { useWindowSize } from '@vueuse/core'
import type { IFileToUpload } from '@/interfaces/entities/IAdmin';
import AdminPostPreview from './components/AdminPostPreview.vue';
import AdminUploadingSection from './components/AdminUploadingSection.vue';

type AdminElementValue = string | IBXFileType | number | string[] | boolean | undefined | Array<{ link: string; name: string }>;

export default defineComponent({
  components: {
    AdminPostPreview,
    Loader,
    AdminComponentTextarea,
    AdminComponentSelect,
    AdminComponentDatePicker,
    AdminComponentInput,
    FileUploader,
    AdminUploadingSection
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
    const activeType: Ref<"noPreview" | "news" | "interview" | "blogs"> = ref('news');
    const buttonIsDisabled = ref(false);
    const isCreateNew = ref(true);
    const { width } = useWindowSize()

    const newElementFiles = ref();

    const toastInstance = useToast();
    const toast = useToastCompose(toastInstance);

    const currentItem: Ref<IPostInner> = ref({ id: 0 });

    const newData: Ref<IPostInner> = ref({ id: 0, images: [chooseImgPlug()] });
    const newFileData = ref<newFileData>({});
    const isMobileScreen = computed(() => ['sm'].includes(screenCheck(width)));

    const inputComponentChecker = (item: IAdminListItem) => {
      if (item.disabled) return;
      switch (true) {
        case (item.data_type == 'str' || item.data_type == 'datetime.datetime') && String(item.field)?.includes('date'):
          return AdminComponentDatePicker
        case (item.data_type == 'str' || item.data_type == 'bool') && 'values' in item:
          return AdminComponentSelect
        case item.data_type == 'str' && item.field?.includes('text'):
          return AdminComponentTextarea
        case item.data_type == 'str':
          return AdminComponentInput
      }
    }

    onMounted(() => {
      if (props.type == 'new') {
        Api.get(`/editor/add/${props.id}`)
          .then((data) => {
            isCreateNew.value = true;
            newElementSkeleton.value = data.fields;
            newElementFiles.value = data.files;
          })
      }
      else reloadElementData(false);
    })

    const reloadElementData = (onlyFiles: boolean = false) => {
      Api.get(`/editor/rendering/${props.elementId}`)
        .then((data) => {
          if (!onlyFiles) {
            isCreateNew.value = false;
            newElementSkeleton.value = data.fields;
            newElementFiles.value = data.files;
          }
          newElementFiles.value = data.files;

          if (data.files.images) {
            newFileData.value.images = data.files.images;
            newData.value.images = data.files.images;
          }
          if (data.files.videos_native) {
            newFileData.value.videos_native = data.files.videos_native;
            newData.value.images = data.files.videos_native;
          }
          if (data.files.documentation) {
            newFileData.value.documentation = data.files.documentation;
            newData.value.documentation = data.files.documentation;
          }
        })
    }

    const applyNewData = async () => {
      buttonIsDisabled.value = true;
      await Api.post(isCreateNew.value ? '/editor/add' : `editor/update/${props.elementId}`, newData.value)
        .then((data) => {
          handleApiResponse(data, toast, 'trySupportError', isCreateNew.value ? 'adminAddElementSuccess' : 'adminApdateElementSuccess')
          router.push({ name: 'adminBlockInner', params: { id: props.id } })
        })
        .catch((error) => {
          handleApiError(error, toast)
        })
        .finally(() => {
          buttonIsDisabled.value = false;
        })
    }

    const handleUpload = (e: IFileToUpload) => {
      console.log(e);

      if (!e || !e.file) return
      const fileToUpload = e.file;
      const formData = new FormData();
      formData.append('file', fileToUpload)
      Api.post(`/editor/upload_file/${props.elementId}`, formData)
        .then(() => reloadElementData(true))
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
      buttonIsDisabled,
      newData,
      newFileData,
      newElementFiles,
      isMobileScreen,
      inputComponentChecker,
      applyNewData,
      handleEmitValueChange,
      handleUpload,
      reloadElementData
    };
  }
});
</script>

<style lang="scss">
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
    transition: flex-direction 0.4s cubic-bezier(0.4, 0, 0.2, 1),
      gap 0.4s cubic-bezier(0.4, 0, 0.2, 1);

    &--preview-full-width {
      flex-direction: column-reverse;
      gap: 20px;
    }
  }

  &__editor {
    display: flex;
    flex-direction: column;
    min-width: 33%;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    transform-origin: center top;

    &--preview-full-width {
      align-items: center;
      align-content: center;
      border-top: 1px solid gainsboro;
      padding-top: 40px;
      transform: translateY(0);
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
      transform: scale(0.95);
    }
  }

  &__field-content {
    transition: all 0.3s ease;

    &--no-transition {
      transition: none !important;
    }
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
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    transform-origin: center top;

    &--full-width {
      position: relative;
      top: auto;
      // transform: translateY(0);
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

    &--disabled {
      background-color: #66666644;

      &:hover {
        background-color: #66666644;
      }
    }

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
      text-align: center;

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
.layout-change-leave-active {
  transition: all 0.2s ease;
}

.layout-change-enter-from,
.layout-change-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.admin-element-inner__editor__loader {
  margin: auto;
}

.file-uploader {
  margin-top: 5px !important;
}

.admin-element-inner__fields {
  &:not(:first-child) {
    margin-top: 15px;
  }
}
</style>
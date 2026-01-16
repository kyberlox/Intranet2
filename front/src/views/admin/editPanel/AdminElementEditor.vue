<template>
<div class="admin-element-inner">
  <div class="admin-element-inner__wrapper mt20"
       :class="{ 'admin-element-inner__wrapper--preview-full-width': previewFullWidth || isMobileScreen }">

    <AdminElementEditorFieldRenderer :isMobileScreen="isMobileScreen"
                                     :previewFullWidth="previewFullWidth"
                                     :activeType="activeType"
                                     :newElementSkeleton="newElementSkeleton"
                                     :newData="newData"
                                     :newFileData="newFileData"
                                     :uploadProgress="uploadProgress"
                                     @handleUserPick="handleUserPick"
                                     @handleEmitValueChange="handleEmitValueChange"
                                     @reportageChanged="(e) => { newData.reports = e }"
                                     @tagsChanged="(e: number[]) => newData.tags = e"
                                     @reloadElementData="(e: boolean) => reloadElementData(e)"
                                     @handleUpload="handleUpload"
                                     @uploadMany="(e) => uploadMany(e)"
                                     @saveEmbed="(e: string[]) => handleUpload(e, true)" />

    <AdminPostPreview :previewFullWidth="previewFullWidth"
                      :isMobileScreen="isMobileScreen"
                      :newFileData="newFileData"
                      :newData="newData"
                      :activeType="activeType"
                      :sectionId="id"
                      :newId="String(newId)"
                      :currentItem="currentItem"
                      @noPreview="previewFullWidth = true"
                      @changePreviewWidth="previewFullWidth = !previewFullWidth" />

  </div>

  <div class="admin-element-inner__actions">
    <button class="primary-button"
            @click="router.push({ name: 'adminBlockInner', params: { id: id } })">
      <span class="admin-element-inner__action-text">Назад</span>
    </button>
    <button @click="applyNewData"
            :disabled="buttonIsDisabled"
            class="admin-element-inner__action-button admin-element-inner__action-button--save">
      <span class="admin-element-inner__action-text">Сохранить</span>
    </button>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, type Ref, computed, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import Api from '@/utils/Api';

import { handleApiError, handleApiResponse } from '@/utils/apiResponseCheck';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import { screenCheck } from '@/utils/screenCheck';
import { useWindowSize } from '@vueuse/core'
import AdminPostPreview from '@/views/admin/editPanel/elementInnerLayout/AdminPostPreview.vue';
import AdminElementEditorFieldRenderer from './AdminElementEditorFieldRenderer.vue';
import { findValInObject } from '@/utils/objectUtil';

import { type IPostInner } from '@/components/tools/common/PostInner.vue';
import type { IAdminListItem, INewFileData, IBXFileType, IFileToUpload } from '@/interfaces/IEntities';
import type { IUserList } from '../components/inputFields/AdminUsersList.vue';
import type { IUsersLoad } from '@/interfaces/IPostFetch';
import type { AxiosProgressEvent } from 'axios';

type AdminElementValue = string | IBXFileType | number | string[] | number[] | boolean | undefined | Array<{ link: string; name: string } | IUserList>;

interface INewDataElement {
  name: string,
  value: string
  field: string
  data_type: string
  values: string[] | boolean[]
}

type PostInnerWithDynamic = IPostInner & {
  [key: string]: unknown;
};

export default defineComponent({
  components: {
    AdminPostPreview,
    AdminElementEditorFieldRenderer
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
    const router = useRouter();
    const { width } = useWindowSize();
    const isMobileScreen = computed(() => ['sm'].includes(screenCheck(width)));
    const newElementSkeleton: Ref<IAdminListItem[]> = ref([]);
    const events = ref<Event[]>([]);
    const previewFullWidth = ref(false);
    const activeType: Ref<"noPreview" | "news" | "interview" | "blogs"> = ref('news');
    const buttonIsDisabled = ref(false);
    const isCreateNew = ref(true);
    const inputKey = ref(0);
    const users = ref<string[]>([]);
    const newId = ref(props.elementId ?? null);
    const currentItem: Ref<IPostInner> = ref({ id: 0 });
    const newData: Ref<IPostInner> = ref({ id: Number(newId.value) });
    const newFileData = ref<INewFileData>({});
    const needToBeDeleted = ref(true);
    const toastInstance = useToast();
    const toast = useToastCompose(toastInstance);
    const usersList = ref<IUserList[]>([]);
    const newEmbedList = ref<string[]>([]);
    const uploadProgress = ref<number>(0);

    onMounted(() => {
      if (props.type == 'new') {
        Api.get(`/editor/add/${props.id}`)
          .then((data) => {
            isCreateNew.value = true;
            newElementSkeleton.value = data.fields;
            newElementSkeleton.value.map((e) => {
              handleEmitValueChange(e, e.value as AdminElementValue)
            })
            newId.value = findValInObject(data, 'id');
            newFileData.value = data.files;
            if (!('section_id' in newData.value)) {
              newData.value.section_id = findValInObject(data, 'section_id');
            }
            newData.value.date_publiction = findValInObject(data, 'date_publiction');
            usersList.value = data.users;
            newData.value.section_id = Number(props.id);

            // newData.value.images = data.files.images;
            newData.value.videos_native = data.files.videos_native;
            newData.value.documentation = data.files.documentation;
          })
      }
      else reloadElementData(false);
    })

    const reloadElementData = (onlyFiles: boolean = false) => {
      Api.get(`/editor/rendering/${newId.value}`)
        .then((data) => {
          if (data.status) {
            router.push({ name: 'admin' })
          }
          else {
            if (!onlyFiles) {
              isCreateNew.value = false;
              newElementSkeleton.value = data.fields;
            }
            // для файлов
            newFileData.value = data.files;
            newData.value.videos_native = data.files.videos_native;
            newData.value.videos_embed = data.files.videos_embed;
            newData.value.documentation = data.files.documentation;
            // для превьюх
            if (data.files?.images && data.files?.images[0]?.file_url) {
              newData.value.preview_file_url = data.files?.images[0]?.file_url
            }
            data.fields.forEach((e: INewDataElement) => {
              if ('value' in e && e.value && e.field) {
                (newData.value as PostInnerWithDynamic)[e.field] = e.value;
              }
            })
          }
        })
    }

    const applyNewData = async () => {
      needToBeDeleted.value = false;
      const apiRoutePrefix = isCreateNew.value ? `/editor/add` : `editor/update`;
      buttonIsDisabled.value = true;

      if (newEmbedList.value.length) {
        await Api.post('file/upload_link', { art_id: isCreateNew.value ? newId.value : props.elementId, links: newEmbedList.value })
      }

      await Api.post((`${apiRoutePrefix}/${newId.value}`), newData.value)
        .then((data) => {
          handleApiResponse(data, toast, 'trySupportError', isCreateNew.value ? 'adminAddElementSuccess' : 'adminUpdateElementSuccess')
          router.push({ name: 'adminBlockInner', params: { id: props.id } })
        })
        .catch((error) => {
          handleApiError(error, toast)
        })
        .finally(() => {
          buttonIsDisabled.value = false;
        })
    }

    const handleUpload = (e: IFileToUpload | string[], embed: boolean = false) => {
      const idToUpload = isCreateNew.value ? newId.value : props.elementId;

      if (embed) {
        newEmbedList.value = (e as string[]);
      }
      else {
        if (!e) return
        if (!embed && 'file' in e) {
          const formData = new FormData()
          formData.append('file', e.file);
          Api.post(`/editor/upload_file/${idToUpload}`, formData)
            .finally(() => reloadElementData(true))
        }
      }
    }

    const checkUploadProgress = (progressEvent: AxiosProgressEvent) => {
      if (progressEvent.lengthComputable && progressEvent.total && progressEvent.total > 0) {
        uploadProgress.value = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
      }
    }

    const uploadMany = (e: IFileToUpload[]) => {
      const idToUpload = isCreateNew.value ? newId.value : props.elementId;
      const formData = new FormData()
      e.forEach((e) => {
        formData.append('files', e.file);
      })

      Api.post(`/editor/upload_files/${idToUpload}`, formData, { onUploadProgress: checkUploadProgress })
        .finally(() => {
          uploadProgress.value = 0;
          reloadElementData(true);
        })
    }


    const handleEmitValueChange = (item: IAdminListItem, value: AdminElementValue) => {
      console.log(value)
      if (item.field) {
        newData.value = {
          ...newData.value,
          [item.field]: value
        };
      }
    };

    const handleUserPick = (userId: number) => {
      Api.get(`editor/get_user_info/${props.id}/${newId.value}/${userId}`)
        .then((data) => {
          if (data) {
            reloadElementData(false)
          }
        })
    }

    const handleUsersPick = (uuid: string, type: ('add' | 'remove') = 'add') => {
      if (type == 'add') {
        if (!users.value.includes(uuid))
          users.value.push(uuid)
      }
      else {
        users.value.length = 0
        usersList.value.map((e) => {
          if (Number(e.id) !== Number(uuid)) {
            users.value.push(String(e.id))
          }
        })
      }

      const usersBody: IUsersLoad = { art_id: newId.value, users_id: users.value }
      Api.post(`editor/get_users_info`, usersBody)
        .then((data) => {
          if (data) {
            reloadElementData(false)
          }
        })
    }

    onUnmounted(async () => {
      if (needToBeDeleted.value && isCreateNew.value) {
        await Api.delete(`editor/del/${newId.value}`)
      }
    })

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
      isMobileScreen,
      newId,
      inputKey,
      uploadProgress,
      handleUsersPick,
      handleUserPick,
      applyNewData,
      handleEmitValueChange,
      handleUpload,
      uploadMany,
      reloadElementData,
    };
  }
});
</script>

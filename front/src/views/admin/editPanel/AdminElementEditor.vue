<template>
<div class="admin-element-inner">
  <div class="admin-element-inner__wrapper mt20"
       :class="{
        'admin-element-inner__wrapper--preview-full-width':
          previewFullWidth || isMobileScreen,
      }">
    <AdminElementEditorFieldRenderer :isMobileScreen="isMobileScreen"
                                     :previewFullWidth="previewFullWidth"
                                     :activeType="activeType"
                                     :newElementSkeleton="newElementSkeleton"
                                     :newData="newData"
                                     :newFileData="newFileData"
                                     :uploadProgress="uploadProgress"
                                     @handleUserPick="handleUserPick"
                                     @handleUsersPick="handleUsersPick"
                                     @handleEmitValueChange="handleEmitValueChange"
                                     @reportageChanged="(e) => {
                                      newData.reports = e;
                                    }"
                                     @tagsChanged="(e: number[]) => newData.tags = e"
                                     @reloadElementData="(e: boolean) => reloadElementData(e)"
                                     @handleUpload="handleUpload"
                                     @uploadMany="(e) => uploadMany(e)"
                                     @visibilityChanged="(newVision) => (artVision = newVision)"
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
            class="admin-element-inner__action-button admin-element-inner__action-button--save">
      <span class="admin-element-inner__action-text">Сохранить</span>
    </button>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, type Ref, computed, onUnmounted, watch } from 'vue';
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
import type { IUserList } from '@/components/tools/common/SearchList.vue';
import type { IUsersLoad } from '@/interfaces/IPostFetch';
import type { AxiosError, AxiosProgressEvent } from 'axios';
import { featureFlags } from '@/assets/static/featureFlags';

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
    const isCreateNew = ref(true);
    const inputKey = ref(0);
    const users = ref<string[]>([]);
    const newId = ref(props.elementId ?? null);
    const currentItem: Ref<IPostInner> = ref({ id: 0 });
    const newData: Ref<IPostInner> = ref({ id: Number(newId.value) });
    const newFileData = ref<INewFileData>({});
    const toastInstance = useToast();
    const toast = useToastCompose(toastInstance);
    const usersList = ref<IUserList[]>([]);
    const newEmbedList = ref<string[]>([]);
    const uploadProgress = ref<number>(0);
    const artVision = ref([]);

    onMounted(async () => {
      if (props.type == 'new') {
        try {
          const data = await Api.get(`/editor/add/${props.id}`)
          isCreateNew.value = true;
          newElementSkeleton.value = data.fields;
          newElementSkeleton.value.map((e) => {
            handleEmitValueChange(e, e.value as AdminElementValue)
          })
          newId.value = (findValInObject(data, 'id') as string);
          newFileData.value = data.files;
          if (!('section_id' in newData.value)) {
            newData.value.section_id = Number(findValInObject(data, 'section_id'));
          }
          // newData.value.date_publiction = findValInObject(data, 'date_publiction') as string;
          usersList.value = data.users;
          newData.value.section_id = Number(props.id);

          // newData.value.images = data.files.images;
          newData.value.videos_native = data.files.videos_native || [];
          newData.value.documentation = data.files.documentation || [];
        }
        catch (error) {
          console.error(error);
        }
      }
      else reloadElementData(false);
    })

    const reloadElementData = async (onlyFiles: boolean = false) => {
      try {
        const data = await Api.get(`/editor/rendering/${newId.value}`)
        if (typeof data == 'object' && 'status' in data && data.status) {
          router.push({ name: 'admin' })
        }
        else {
          if (!onlyFiles) {
            isCreateNew.value = false;
            newElementSkeleton.value = data.fields;
          }

          const usersVal = findValInObject(data, 'users') as IUserList[] || [];
          if (usersVal.length) {
            users.value = usersVal.map((e: IUserList) => String(e.id)) || [];
          }
          newData.value.implementer = findValInObject(data, 'implementer') as string[] || [];
          newData.value.integrator = findValInObject(data, 'integrator') as string[] || [];
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
      } catch (error) {
        console.error(error);
      }
    }

    const applyNewData = async () => {
      const apiRoutePrefix = isCreateNew.value ? `/editor/add` : `editor/update`;

      if (artVision.value && newElementSkeleton.value.find(e => e.field == 'vision')) {
        newData.value.vision = artVision.value
        try {
          await Api.put(`/fields_visions/set_art_to_visions/${newId.value}`, artVision.value.map(e => Number(e)))
        } catch (error) {
          handleApiError((error as AxiosError), toast)
        }
      }
      // проверка на выставление областей видимости у афишы и корп событиях
      if ((props.id == '53' || props.id == '51' || props.id == '31') && featureFlags.visibleArea && (!newData.value?.vision?.length || !('vision' in newData.value))) {
        toast.showError('noVisionError');
      }
      else
        try {
          await Api.post('file/upload_link', { art_id: newId.value, links: newEmbedList.value })
          const data = await Api.post((`${apiRoutePrefix}/${newId.value}`), newData.value)
          handleApiResponse(data, toast, 'trySupportError', isCreateNew.value ? 'adminAddElementSuccess' : 'adminUpdateElementSuccess')
          router.push({ name: 'adminBlockInner', params: { id: props.id } })
        } catch (error) {
          handleApiError((error as AxiosError), toast)
        }
    }

    const handleUpload = async (e: IFileToUpload | string[], embed: boolean = false) => {
      const idToUpload = newId.value;

      if (embed) {
        newEmbedList.value = (e as string[]);
      }
      else {
        if (!e) return
        if (!embed && 'file' in e) {
          const formData = new FormData()
          formData.append('file', e.file);
          try {
            await Api.post(`/editor/upload_file/${idToUpload}`, formData)
          } finally {
            reloadElementData(true)
          }
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

    const uploadMany = async (e: IFileToUpload[]) => {
      const idToUpload = newId.value;
      const formData = new FormData()
      e.forEach((e) => {
        formData.append('files', e.file);
      })
      try {
        await Api.post(`/editor/upload_files/${idToUpload}`, formData, { onUploadProgress: checkUploadProgress })

      } catch (error) {
        console.error(error)
      } finally {
        uploadProgress.value = 0;
        reloadElementData(true);
      }
    }

    const handleEmitValueChange = (item: IAdminListItem, value: AdminElementValue, name: string = '') => {
      if (item.field) {
        newData.value = {
          ...newData.value,
          [item.field]: value
        };
        if (item.field == 'manufacture_id') {
          const targetEl = newElementSkeleton.value.find(e => e.field == 'company');
          if (targetEl)
            targetEl.value = name;
        }
      }
    };

    const handleUserPick = async (userId: number, field: string) => {
      try {
        const data = await Api.get(`editor/get_user_info/${props.id}/${newId.value}/${userId}${`?field=${field}`}`)
        if (data) {
          reloadElementData(false)
        }
      } catch (error) {
        console.error(error)
      }
    }

    const handleUsersPick = async (uuid: string | number, type: ('add' | 'remove' | 'fetchRemove') = 'add') => {
      const updateUsersInfo = async () => {
        const usersBody: IUsersLoad = { art_id: newId.value, users_id: users.value }
        try {
          const data = await Api.post(`editor/get_users_info`, usersBody)
          if (data) {
            reloadElementData(false)
          }
        }
        catch (error) {
          console.error(error)
        }
      }

      if (type == 'add') {
        if (!users.value.includes(String(uuid))) {
          users.value.push(String(uuid));
          updateUsersInfo();
        }
      }
      else if (type == 'remove') {
        users.value = users.value.filter((e) => e !== uuid);
        updateUsersInfo();
      }
      else if (type == 'fetchRemove') {
        try {
          const data = await Api.get(`editor/get_user_info/${props.id}/${newId.value}/null`)
          if (data) {
            reloadElementData(false)
          }
        } catch (error) {
          console.error(error)
        }
      }


      onUnmounted(() => {
        if (!newData.value.name && !newData.value.content_text && newData.value.content_text?.length == 0 && !newData.value.videos_embed?.length && !newData.value.videos_native?.length && isCreateNew.value) {
          Api.delete(`editor/del/${newId.value}`)
        }
      })
    }

    return {
      events,
      router,
      currentItem,
      previewFullWidth,
      activeType,
      newElementSkeleton,
      newData,
      newFileData,
      isMobileScreen,
      newId,
      inputKey,
      uploadProgress,
      artVision,
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

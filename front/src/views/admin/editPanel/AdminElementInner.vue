<template>
<div class="admin-element-inner">
  <div class="admin-element-inner__wrapper mt20"
       :class="{ 'admin-element-inner__wrapper--preview-full-width': previewFullWidth || isMobileScreen }">
    <div v-if="newElementSkeleton.length"
         :class="['admin-element-inner__editor',
          { 'admin-element-inner__editor--preview-full-width': previewFullWidth || isMobileScreen },
          { 'admin-element-inner__editor--no-preview': activeType == 'noPreview' }
        ]">
      <div v-for="(item, index) in newElementSkeleton"
           class="admin-element-inner__field"
           :key="index">


        <AdminEditUserSearch v-if="item.data_type == 'search_by_uuid'"
                             @userPicked="handleUserPick" />

        <Component :is="inputComponentChecker(item)"
                   :item="item"
                   :type="item.data_type == 'int' ? 'number' : 'text'"
                   @pick="(value: string) => handleEmitValueChange(item, value)" />

        <img v-if="item.field == 'photo_file_url'"
             :src="(item.value as string)" />

        <AdminEditReportage v-if="item.field == 'reports'"
                            :item="(item.value as IReportage[])"
                            @pick="handleReportChange" />
      </div>

      <div class="admin-element-inner__field mt10">
        <AdminEditInput v-if="newFileData.videos_embed"
                        :item="{ name: 'Видео с источников', field: 'videos_embed', values: [{ name: '', id: '' }] }"
                        @pick="(value: string) => handleEmitValueChange({ name: 'Видео с источников', field: 'videos_embed' }, value)" />
      </div>
      <AdminUploadingSection class="mt10"
                             :newFileData="newFileData"
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
                      :sectionId="id"
                      :newId="String(newId)"
                      :currentItem="currentItem"
                      @noPreview="previewFullWidth = true"
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
import { defineComponent, onMounted, ref, type Ref, computed, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import Api from '@/utils/Api';
import AdminEditSelect from '@/views/admin/components/inputFields/AdminEditSelect.vue';
import AdminEditTextarea from '@/views/admin/components/inputFields/AdminEditTextarea.vue';
import AdminEditDatePicker from '@/views/admin/components/inputFields/AdminEditDatePicker.vue';
import AdminEditInput from '@/views/admin/components/inputFields/AdminEditInput.vue';
import AdminEditReportage from '@/views/admin/components/inputFields/AdminEditReportage.vue';
import Loader from '@/components/layout/Loader.vue';
import { handleApiError, handleApiResponse } from '@/utils/ApiResponseCheck';
import FileUploader from '@/components/tools/common/FileUploader.vue';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import { screenCheck } from '@/utils/screenCheck';
import { useWindowSize } from '@vueuse/core'
import AdminPostPreview from '@/views/admin/editPanel/elementInnerLayout/AdminPostPreview.vue';
import AdminUploadingSection from '@/views/admin/editPanel/elementInnerLayout/AdminUploadingSection.vue';
import AdminEditUserSearch from '@/views/admin/components/inputFields/AdminEditUserSearch.vue';

import { type IPostInner } from '@/components/tools/common/PostInner.vue';
import type { IAdminListItem, INewFileData, IReportage, IBXFileType, IFileToUpload } from '@/interfaces/IEntities';

type AdminElementValue = string | IBXFileType | number | string[] | boolean | undefined | Array<{ link: string; name: string }>;

export default defineComponent({
  components: {
    AdminPostPreview,
    Loader,
    AdminEditTextarea,
    AdminEditSelect,
    AdminEditDatePicker,
    AdminEditReportage,
    AdminEditInput,
    AdminEditUserSearch,
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
    const { width } = useWindowSize();
    const inputKey = ref(0);

    const newId = ref(props.elementId ?? null);

    const toastInstance = useToast();
    const toast = useToastCompose(toastInstance);

    const currentItem: Ref<IPostInner> = ref({ id: 0 });

    const newData: Ref<IPostInner> = ref({ id: Number(newId.value) });
    const newFileData = ref<INewFileData>({});
    const isMobileScreen = computed(() => ['sm'].includes(screenCheck(width)));

    const needToBeDeleted = ref(true);

    const inputComponentChecker = (item: IAdminListItem) => {
      if (item.disabled) return;
      switch (true) {
        case (item.data_type == 'str' || item.data_type == 'datetime.datetime') && String(item.field)?.includes('date'):
          return AdminEditDatePicker
        case (item.data_type == 'str' || item.data_type == 'bool') && 'values' in item:
          return AdminEditSelect
        case item.data_type == 'str' && item.field?.includes('text'):
          return AdminEditTextarea
        case item.data_type == 'str' || item.data_type == 'int':
          return AdminEditInput
      }
    }
    onMounted(() => {
      if (props.type == 'new') {
        Api.get(`/editor/add/${props.id}`)
          .then((data) => {
            isCreateNew.value = true;
            newElementSkeleton.value = data.fields;
            newElementSkeleton.value.map((e) => {
              handleEmitValueChange(e, e.value)
            })
            newId.value = data.fields.find((e: IAdminListItem) => e.field == 'id').value;
            newFileData.value = data.files;
            if (!('section_id' in newData.value)) {
              newData.value.section_id = data.fields.find((e: IAdminListItem) => e.field == 'section_id').value;
            }

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
          if (!onlyFiles) {
            isCreateNew.value = false;
            newElementSkeleton.value = data.fields;
          }
          newId.value = data.fields.find((e: IAdminListItem) => e.field == 'id').value;
          newFileData.value = data.files;
          // для превьюх
          if (data.files?.images && data.files?.images[0]?.file_url) {
            newData.value.preview_file_url = data.files?.images[0]?.file_url
          }
          // для привязки по uid к статьям
          const targetDepartment = data.fields.find((e: { field: string }) => e.field == 'department')

          if (targetDepartment) {
            newData.value.department = targetDepartment.value
          }
          // newData.value.images = data.files.images;
          newData.value.videos_native = data.files.videos_native;
          newData.value.documentation = data.files.documentation;
        })
    }

    const applyNewData = async () => {
      needToBeDeleted.value = false;
      const apiRoutePrefix = isCreateNew.value ? `/editor/add` : `editor/update`;
      buttonIsDisabled.value = true;
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

    onUnmounted(async () => {
      if (needToBeDeleted.value && isCreateNew.value) {
        await Api.delete(`editor/del/${newId.value}`)
      }
    })

    const handleUpload = (e: IFileToUpload) => {
      const idToUpload = isCreateNew.value ? newId.value : props.elementId
      if (!e || !e.file) return

      const formData = new FormData()
      formData.append('file', e.file)

      Api.post(`/editor/upload_file/${idToUpload}`, formData)
        .finally(() => reloadElementData(true))
    }

    const handleEmitValueChange = (item: IAdminListItem, value: AdminElementValue) => {
      if (item.field) {
        newData.value = {
          ...newData.value,
          [item.field]: value
        };
      }
    };

    const handleReportChange = (item: IReportage[]) => {
      newData.value.reports = item
    }

    const handleUserPick = (userId: number) => {
      Api.get(`editor/get_user_info/${props.id}/${newId.value}/${userId}`)
        .then((data) => {
          if (data) {
            reloadElementData(false)
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
      buttonIsDisabled,
      newData,
      newFileData,
      isMobileScreen,
      newId,
      inputKey,
      handleUserPick,
      inputComponentChecker,
      applyNewData,
      handleEmitValueChange,
      handleUpload,
      reloadElementData,
      handleReportChange
    };
  }
});
</script>
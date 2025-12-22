<template>
<div v-if="newElementSkeleton?.length"
     :class="['admin-element-inner__editor',
        { 'admin-element-inner__editor--preview-full-width': previewFullWidth || isMobileScreen },
        { 'admin-element-inner__editor--no-preview': activeType == 'noPreview' }
    ]">
    <div v-for="(item, index) in newElementSkeleton"
         class="admin-element-inner__field"
         :key="index">

        <AdminEditUserSearch v-if="item.data_type == 'search_by_uuids' || item.data_type == 'search_by_uuid'"
                             :type="item.data_type"
                             @userPicked="(e) => $emit('handleUserPick', e)"
                             @usersPicked="(e) => $emit('handleUsersPick', e)" />

        <AdminUsersList v-if="item.field == 'users'"
                        :users="(item.value as IUserList[])"
                        @removeUser="(id: number) => $emit('handleUsersPick', String(id), 'remove')" />

        <AdminEditInputMulti v-else-if="item.field == 'reports'"
                             :item="(item.value as IReportage[])"
                             @pick="(val) => $emit('reportageChanged', val)" />

        <AdminEditTags v-if="item.field == 'all_tags'"
                       :currentTags="(newElementSkeleton.find((e) => e.field == 'tags')?.value as number[])"
                       :allTags="(item.values as ITag[])"
                       @tagsChanged="(e: number[]) => $emit('tagschanged', e)" />

        <Component v-else
                   :is="inputComponentChecker(item)"
                   :item="item"
                   :type="item.data_type == 'int' ? 'number' : 'text'"
                   @pick="(value: string) => $emit('handleEmitValueChange', item, value)" />

        <img v-if="item.field == 'photo_file_url'"
             :src="(item.value as string)" />

    </div>

    <div class="admin-element-inner__field mt10">
        <!-- <AdminEditInput v-if="newFileData?.videos_embed"
                        :item="{ name: 'Видео с источников', field: 'videos_embed', values: [{ name: '', id: '' }] }"
                        @pick="(value: string) => $emit('handleEmitValueChange', { name: 'Видео с источников', field: 'videos_embed' }, value)" /> -->

        <AdminEditInputMulti v-if="newFileData?.videos_embed"
                             :title="'Видео с источников'"
                             :item="newFileData?.videos_embed"
                             @pick="(value: string) => $emit('handleEmitValueChange', { name: 'Видео с источников', field: 'videos_embed' }, value)" />

    </div>
    <AdminUploadingSection class="mt10"
                           :newFileData="newFileData"
                           :newData="newData"
                           @reloadData="$emit('reloadElementData', true)"
                           @handleUpload="(e: IFileToUpload) => $emit('handleUpload', e)" />
</div>

<div v-else
     class="admin-element-inner__editor">
    <Loader class="admin-element-inner__editor__loader loader" />
</div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";
import { type IPostInner } from '@/components/tools/common/PostInner.vue';

import type { IAdminListItem, IReportage, INewFileData } from "@/interfaces/IEntities";
import type { ITag } from "@/interfaces/entities/ITag";
import type { IUserList } from "../components/inputFields/AdminUsersList.vue";
import AdminEditSelect from '@/views/admin/components/inputFields/AdminEditSelect.vue';
import AdminEditTextarea from '@/views/admin/components/inputFields/AdminEditTextarea.vue';
import AdminEditDatePicker from '@/views/admin/components/inputFields/AdminEditDatePicker.vue';
import AdminEditInput from '@/views/admin/components/inputFields/AdminEditInput.vue';
import AdminUploadingSection from "./elementInnerLayout/AdminUploadingSection.vue";
import AdminEditUserSearch from "../components/inputFields/AdminEditUserSearch.vue";
import AdminEditInputMulti from "../components/inputFields/AdminEditInputMulti.vue";
import FileUploader from "@/components/tools/common/FileUploader.vue";
import AdminUsersList from "../components/inputFields/AdminUsersList.vue";
import AdminEditTags from "../components/inputFields/AdminEditTags.vue";
import Loader from "@/components/layout/Loader.vue";
import { type IFileToUpload } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        AdminEditSelect,
        AdminEditTextarea,
        AdminEditDatePicker,
        AdminEditInput,
        Loader,
        AdminEditInputMulti,
        AdminEditUserSearch,
        FileUploader,
        AdminUploadingSection,
        AdminUsersList,
        AdminEditTags,
    },
    emits: ['handleUserPick', 'handleUsersPick', 'reportageChanged', 'tagschanged', 'handleEmitValueChange', 'reloadElementData', 'handleUpload'],
    props: {
        isMobileScreen: {
            type: Boolean
        },
        previewFullWidth: {
            type: Boolean
        },
        activeType: {
            type: String as PropType<"noPreview" | "news" | "interview" | "blogs">
        },
        newElementSkeleton: {
            type: Array<IAdminListItem>
        },
        newData: {
            type: Object as PropType<IPostInner>
        },
        newFileData: {
            type: Object as PropType<INewFileData>
        }
    },
    setup() {
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

        return {
            inputComponentChecker
        }
    }
})
</script>
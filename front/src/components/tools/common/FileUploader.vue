<template>
<div class="file-uploader">
    <div class="file-uploader__drop-zone"
         :class="{ 'file-uploader__drop-zone--dragover': isDragOver }"
         @drop="handleDrop"
         @dragover.prevent="handleDragOver"
         @dragleave="handleDragLeave"
         @click="triggerFileInput">

        <input ref="fileInput"
               type="file"
               class="file-uploader__input"
               @change="(e) => $emit('upload', (useFile.handleFileSelect(e)))"
               multiple />

        <div v-if="!uploadedFiles.length"
             class="file-uploader__placeholder">
            <p class="file-uploader__text">Перетащите файл сюда или нажмите для выбора</p>
        </div>

        <div class="file-uploader__preview-list"
             :class="{ 'file-uploader__preview-list--video': uploadType == 'videos_native' }">
            <div v-for="(item, index) in existFiles"
                 :key="index"
                 class="file-uploader__preview-item">
                <video v-if="uploadType == 'videos_native' && item.file_url"
                       class="file-uploader__preview-video"
                       :src="item.file_url"
                       @click.stop.prevent="openFile(item.file_url)"
                       controls>
                    Ваш браузер не поддерживает видео.
                </video>
                <img v-if="uploadType == 'images' && item.file_url"
                     class="file-uploader__preview-img"
                     :src="item.file_url"
                     @click.stop.prevent="openFile(item.file_url)" />
                <div v-if="uploadType == 'documentation' && item.file_url"
                     class="file-uploader__preview-doc">
                    <span @click.stop.prevent="openFile(item.file_url)"
                          v-if="item.original_name">{{ item.original_name }}</span>
                    <DocIcon />
                </div>

                <button class="file-uploader__remove-btn"
                        @click.stop="removeItem(String(item.id))">
                    <RemoveIcon />
                </button>
            </div>
            <div class="file-uploader__preview-list__loader"
                 v-if="isUploading">
                <Loader />
            </div>

        </div>
    </div>

    <!-- <div v-if="isUploading"
         class="file-uploader__progress">
        <div class="file-uploader__progress-bar">
            <div class="file-uploader__progress-fill"
                 :style="{ width: uploadProgress + '%' }"></div>
        </div>
        <span class="file-uploader__progress-text">{{ uploadProgress }}%</span>
    </div> -->

</div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, type PropType } from 'vue';
import RemoveIcon from '@/assets/icons/admin/RemoveIcon.svg?component';
import DocIcon from '@/assets/icons/posts/DocIcon.svg?component';
import { useFileUtil } from '@/composables/useFile';
import Api from '@/utils/Api';
import Loader from '@/components/layout/Loader.vue';
import type { IBXFileType, IFileToUpload } from '@/interfaces/IEntities';

export default defineComponent({
    name: 'FileUploader',
    props: {
        uploadType: {
            type: String as PropType<'images' | 'documentation' | 'videos_native'>,
            default: 'images'
        },
        existFiles: {
            type: Array<IBXFileType>
        }
    },
    components: {
        RemoveIcon,
        DocIcon,
        Loader
    },
    emits: ['upload', 'remove', 'reloadData'],
    setup(props, { emit }) {
        const fileInput = ref<HTMLInputElement>();
        const uploadedFiles = ref<IFileToUpload[]>([]);
        const isDragOver = ref(false);
        const isUploading = ref(false);
        const uploadProgress = ref(0);
        const error = ref('');
        const useFile = useFileUtil(props.uploadType);

        const handleDrop = (event: DragEvent) => {
            event.preventDefault();
            isDragOver.value = false;

            if (event.dataTransfer?.files) {
                const processResult = useFile.processFiles(event.dataTransfer.files);

                if (typeof processResult == 'string') {
                    error.value = processResult;
                }
                else {
                    uploadedFiles.value.push(processResult as IFileToUpload);
                    emit('upload', processResult);
                    isUploading.value = true
                }
            }
        };

        watch((() => props.existFiles), () => {
            if (props.existFiles?.length)
                isUploading.value = false
        }, { deep: true })

        const handleDragOver = (event: DragEvent) => {
            event.preventDefault();
            isDragOver.value = true;
        };

        const handleDragLeave = () => {
            isDragOver.value = false;
        };

        const triggerFileInput = () => {
            fileInput.value?.click();
        };

        const removeItem = (id: string) => {
            Api.delete(`editor/delete_file/${id}`)
                .then(() => emit('reloadData'))
        };

        return {
            fileInput,
            uploadedFiles,
            isDragOver,
            isUploading,
            uploadProgress,
            error,
            useFile,
            handleDrop,
            handleDragOver,
            handleDragLeave,
            triggerFileInput,
            removeItem,
            openFile: (url: string) => window.open(url, '_blank')
        };
    }
});
</script>
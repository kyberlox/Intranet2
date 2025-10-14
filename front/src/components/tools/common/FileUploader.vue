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
               @change="handleFormFileSelect"
               :multiple="quantity === 'many'" />

        <div v-if="!existFiles?.length && !uploadedFiles.length"
             class="file-uploader__placeholder">
            <p class="file-uploader__text">
                {{ quantity === 'many' ? 'Перетащите файлы сюда или нажмите для выбора'
                    : 'Перетащите файл сюда или нажмите для выбора' }}
            </p>
        </div>

        <div class="file-uploader__preview-list"
             :class="{ 'file-uploader__preview-list--video': uploadType == 'videos_native' }">
            <!-- Существующие файлы -->
            <div v-for="(item, index) in existFiles"
                 :key="'exist-' + index"
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
                          v-if="item.original_name">
                        {{ item.original_name }}
                    </span>
                    <DocIcon />
                </div>

                <button class="file-uploader__remove-btn"
                        @click.stop="removeItem(String(item.id))">
                    <RemoveIcon />
                </button>
            </div>

            <!-- Новые  файлы -->
            <div v-for="(file, index) in uploadedFiles"
                 :key="'uploading-' + index"
                 class="file-uploader__preview-item">
                <div v-if="uploadType === 'images'"
                     class="file-uploader__preview-img">
                    <img :src="file.url"
                         :alt="file.name" />
                </div>
                <div v-else-if="uploadType === 'videos_native'"
                     class="file-uploader__preview-video">
                    <video :src="file.url"
                           controls></video>
                </div>
                <div v-else
                     class="file-uploader__preview-doc">
                    <span>{{ file.name }}</span>
                    <DocIcon />
                </div>
                <div class="file-uploader__uploading-overlay"
                     v-if="isUploading">
                    <Loader />
                </div>
            </div>

            <div class="file-uploader__preview-item"
                 v-if="isUploading && !uploadedFiles.length">
                <Loader />
            </div>
        </div>
    </div>
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
            type: Array as PropType<IBXFileType[]>
        },
        quantity: {
            type: String as PropType<('one' | 'many')>,
            default: () => 'many'
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
        const error = ref('');
        const useFile = useFileUtil(props.uploadType);

        const handleDrop = (event: DragEvent) => {
            event.preventDefault();
            isDragOver.value = false;

            if (event.dataTransfer?.files) {
                processFiles(event.dataTransfer.files);
            }
        };

        const handleFormFileSelect = (e: Event) => {
            const input = e.target as HTMLInputElement;
            if (input.files) {
                processFiles(input.files);
            }
        };

        const processFiles = (files: FileList) => {
            isUploading.value = true;

            const processResult = useFile.processFiles(files);

            if (typeof processResult === 'string') {
                error.value = processResult;
                isUploading.value = false;
                return;
            }

            if (props.quantity === 'one') {
                const target = [(processResult as IFileToUpload[])[0]]
                uploadedFiles.value = target;
                emit('upload', target, props.uploadType);
            } else {
                uploadedFiles.value = processResult as IFileToUpload[];
                (processResult as IFileToUpload[]).forEach(file => {
                    emit('upload', file, props.uploadType);
                });
            }

            startWatchForUpload();

            if (fileInput.value) {
                fileInput.value.value = '';
            }
        };

        const triggerFileInput = () => {
            fileInput.value?.click();
        };

        const removeItem = (id: string) => {
            Api.delete(`editor/delete_file/${id}`)
                .then(() => {
                    emit('reloadData');
                });
        };

        const startWatchForUpload = () => {
            const existFilesState = props.existFiles?.length;

            watch(() => props.existFiles, (newFiles) => {
                if (newFiles?.length !== existFilesState) {
                    isUploading.value = false;
                    uploadedFiles.value = [];
                }
            }, { once: true });
        };

        return {
            fileInput,
            uploadedFiles,
            isDragOver,
            isUploading,
            error,
            handleDrop,
            handleDragOver: (event: DragEvent) => {
                event.preventDefault();
                isDragOver.value = true;
            },
            handleDragLeave: () => {
                isDragOver.value = false;
            },
            handleFormFileSelect,
            triggerFileInput,
            removeItem,
            openFile: (url: string) => window.open(url, '_blank')
        };
    }
});
</script>

<style scoped>
.file-uploader__uploading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    max-height: 150px;
}

.file-uploader__preview-item {
    position: relative;
    max-height: 150px;
}
</style>
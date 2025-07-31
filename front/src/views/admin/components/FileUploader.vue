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
                   @change="handleFileSelect"
                   multiple />

            <div v-if="!uploadedFiles.length"
                 class="file-uploader__placeholder">
                <p class="file-uploader__text">Перетащите файл сюда или нажмите для выбора</p>
            </div>

            <div class="file-uploader__preview-list"
                 :class="{ 'file-uploader__preview-list--video': uploadType == 'videoNative' }">
                <div v-for="(item, index) in existFiles"
                     :key="index"
                     class="file-uploader__preview-item">
                    <video v-if="uploadType == 'videoNative'"
                           @click.stop.prevent=""
                           class="file-uploader__preview-video"
                           :src="item"
                           controls>
                        Ваш браузер не поддерживает видео.
                    </video>
                    <img v-if="uploadType == 'img'"
                         class="file-uploader__preview-img"
                         :src="item" />
                    <div class="file-uploader__preview-doc"
                         v-if="uploadType == 'docs'">
                        <span v-if="item.original_name">{{ item.original_name }}</span>
                        <DocIcon />
                    </div>

                    <button class="file-uploader__remove-btn"
                            @click.stop="removeVideo(index)">
                        <RemoveIcon />
                    </button>
                </div>
            </div>
        </div>

        <div v-if="isUploading"
             class="file-uploader__progress">
            <div class="file-uploader__progress-bar">
                <div class="file-uploader__progress-fill"
                     :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <span class="file-uploader__progress-text">{{ uploadProgress }}%</span>
        </div>

        <div v-if="error"
             class="file-uploader__error">
            {{ error }}
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, type PropType, type Ref } from 'vue';
import { allowedTypes } from '@/assets/static/uploadAllowedTypes';
import RemoveIcon from '@/assets/icons/admin/RemoveIcon.svg?component';
import DocIcon from '@/assets/icons/posts/DocIcon.svg?component'

interface IFileToUpload {
    name: string;
    size: number;
    url: string;
    file: File;
}

export default defineComponent({
    name: 'VideoUploader',
    props: {
        uploadType: {
            type: String as PropType<'img' | 'docs' | 'videoNative'>,
            default: 'img'
        },
        existFiles: {
            type: Array<string>
        }
    },
    components: {
        RemoveIcon,
        DocIcon
    },
    emits: ['upload', 'remove'],
    setup(props, { emit }) {
        const fileInput = ref<HTMLInputElement>();
        const uploadedFiles = ref<IFileToUpload[]>([]);
        const isDragOver = ref(false);
        const isUploading = ref(true);
        const uploadProgress = ref(0);
        const error = ref('');

        const allowedType: Ref<string[]> = ref(allowedTypes[props.uploadType]);

        const validateFile = (file: File): boolean => {
            if (!allowedType.value.includes(file.type)) {
                error.value = 'Неподдерживаемый формат файла';
                return false;
            }

            error.value = '';
            return true;
        };

        const processFiles = (files: FileList | File[]) => {
            const fileArray = Array.from(files);

            fileArray.forEach(file => {
                if (validateFile(file)) {
                    const videoFile: IFileToUpload = {
                        name: file.name,
                        size: file.size,
                        url: URL.createObjectURL(file),
                        file: file
                    };

                    uploadedFiles.value.push(videoFile);
                    emit('upload', videoFile);
                }
            });
        };

        const handleFileSelect = (event: Event) => {
            const target = event.target as HTMLInputElement;
            if (target.files) {
                processFiles(target.files);
            }
        };

        const handleDrop = (event: DragEvent) => {
            event.preventDefault();
            isDragOver.value = false;

            if (event.dataTransfer?.files) {
                processFiles(event.dataTransfer.files);
            }
        };

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

        const removeVideo = (index: number) => {
            const file = uploadedFiles.value[index];
            URL.revokeObjectURL(file.url);
            uploadedFiles.value.splice(index, 1);
            emit('remove', file);
        };

        return {
            fileInput,
            uploadedFiles,
            isDragOver,
            isUploading,
            uploadProgress,
            error,
            handleFileSelect,
            handleDrop,
            handleDragOver,
            handleDragLeave,
            triggerFileInput,
            removeVideo,
        };
    }
});
</script>
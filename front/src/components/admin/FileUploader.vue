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
                   :accept="acceptedFileTypes"
                   @change="handleFileSelect"
                   multiple />

            <div v-if="!uploadedVideos.length"
                 class="file-uploader__placeholder">
                <p class="file-uploader__text">Перетащите файл сюда или нажмите для выбора</p>
                <!-- <p class="file-uploader__hint">Поддерживаемые форматы: MP4, PNG, JPEG, WMV</p> -->
            </div>

            <div v-else-if="uploadType == 'video'"
                 class="file-uploader__preview-list">
                <div v-for="(video, index) in uploadedVideos"
                     :key="index"
                     class="file-uploader__preview-item">
                    <video class="file-uploader__preview-video"
                           :src="video.url"
                           controls
                           preload="metadata">
                        Ваш браузер не поддерживает видео.
                    </video>
                    <div class="file-uploader__preview-info">
                        <span class="file-uploader__preview-name">{{ video.name }}</span>
                        <span class="file-uploader__preview-size">{{ formatFileSize(video.size) }}</span>
                    </div>
                    <button class="file-uploader__remove-btn"
                            @click.stop="removeVideo(index)">
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
import { defineComponent, ref, computed } from 'vue';


interface VideoFile {
    name: string;
    size: number;
    url: string;
    file: File;
}

export default defineComponent({
    name: 'VideoUploader',
    props: {
        uploadType: {
            type: String,
            default: 'img'
        }
    },
    emits: ['upload', 'remove'],
    setup(props, { emit }) {
        const fileInput = ref<HTMLInputElement>();
        const uploadedVideos = ref<VideoFile[]>([]);
        const isDragOver = ref(false);
        const isUploading = ref(true);
        const uploadProgress = ref(0);
        const error = ref('');

        const acceptedFileTypes = computed(() => {
            switch (props.uploadType) {
                case 'video':
                    return 'video/*';
                case 'doc':
                    return '.pdf,.doc,.docx,.txt,.rtf,.odt';
                case 'img':
                    return 'image/*';
                default:
                    return '*';
            }
        });

        const maxFileSize = 100 * 1024 * 1024; // 100MB
        const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/wmv', 'video/webm'];

        const validateFile = (file: File): boolean => {
            if (!allowedTypes.includes(file.type)) {
                error.value = 'Неподдерживаемый формат файла';
                return false;
            }

            if (file.size > maxFileSize) {
                error.value = 'Файл слишком большой (максимум 100MB)';
                return false;
            }

            error.value = '';
            return true;
        };

        const processFiles = (files: FileList | File[]) => {
            const fileArray = Array.from(files);

            fileArray.forEach(file => {
                if (validateFile(file)) {
                    const videoFile: VideoFile = {
                        name: file.name,
                        size: file.size,
                        url: URL.createObjectURL(file),
                        file: file
                    };

                    uploadedVideos.value.push(videoFile);
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
            const video = uploadedVideos.value[index];
            URL.revokeObjectURL(video.url);
            uploadedVideos.value.splice(index, 1);
            emit('remove', video);
        };

        const formatFileSize = (bytes: number): string => {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        };

        return {
            fileInput,
            uploadedVideos,
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
            formatFileSize,
            acceptedFileTypes
        };
    }
});
</script>

<style lang="scss" scoped>
.file-uploader {
    &__drop-zone {
        border: 2px dashed #ddd;
        border-radius: 8px;
        padding: 40px 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;

        &:hover {
            border-color: var(--emk-brand-color);
            background-color: #f8f9ff;
        }

        &--dragover {
            border-color: var(--emk-brand-color);
            background-color: #f0f8ff;
        }
    }

    &__input {
        display: none;
    }

    &__placeholder {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }

    &__icon {
        width: 48px;
        height: 48px;
        color: #666;
    }

    &__text {
        font-size: 16px;
        color: #333;
        margin: 0;
    }

    &__hint {
        font-size: 14px;
        color: #666;
        margin: 0;
    }

    &__preview-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
    }

    &__preview-item {
        position: relative;
        border: 1px solid #ddd;
        border-radius: 8px;
        overflow: hidden;
        background: white;
    }

    &__preview-video {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }

    &__preview-info {
        padding: 10px;
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    &__preview-name {
        font-weight: 500;
        font-size: 14px;
        color: #333;
        word-break: break-word;
    }

    &__preview-size {
        font-size: 12px;
        color: #666;
    }

    &__remove-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: none;
        background: rgba(255, 77, 79, 0.9);
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;

        &:hover {
            background: #ff4d4f;
            transform: scale(1.1);
        }
    }

    &__progress {
        margin-top: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    &__progress-bar {
        flex: 1;
        height: 8px;
        background: #f0f0f0;
        border-radius: 4px;
        overflow: hidden;
    }

    &__progress-fill {
        height: 100%;
        background: var(--emk-brand-color);
        transition: width 0.3s ease;
    }

    &__progress-text {
        font-size: 14px;
        color: #666;
        min-width: 40px;
    }

    &__error {
        margin-top: 10px;
        padding: 10px;
        background: #fff2f0;
        border: 1px solid #ffccc7;
        border-radius: 4px;
        color: #ff4d4f;
        font-size: 14px;
    }
}
</style>
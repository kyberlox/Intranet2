<template>
<div class="admin-element-inner__field"
     v-if="newFileData">
    <div class="admin-element-inner__field"
         v-if="newFileData.images?.length && newFileData.images?.length > 0 && !(newData && 'author' in newData)">
        <p>Превью новости (берется первое загруженное из списка изображений)</p>
        <img :src="newFileData.images[0].file_url" />
    </div>
    <div class="admin-element-inner__fields"
         v-for="itemKey in Object.keys(newFileData)"
         :key="'key' + itemKey">
        <div v-if="newFileData && itemKey !== 'videos_embed'">
            <p class="admin-element-inner__field-title fs-l">
                {{ blockTitle(itemKey) }}
            </p>
            <div>
                <FileUploader @upload="(e) => $emit('handleUpload', e)"
                              @uploadMany="(e) => $emit('uploadMany', e)"
                              @reloadData="$emit('reloadData')"
                              :uploadType="(itemKey as keyof IKeyToWord)"
                              :uploadProgress="uploadProgress"
                              :existFiles="(newFileData[itemKey as keyof IKeyToWord])" />
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, type PropType, computed, ref } from 'vue';
import type { INewFileData } from '@/interfaces/IEntities';
import type { IPostInner } from '@/components/tools/common/PostInner.vue';
import FileUploader from '@/components/tools/common/FileUploader.vue';

interface IKeyToWord {
    images: string,
    videos_native: string,
    documentation: string
}

export default defineComponent({
    components: {
        FileUploader,
    },
    props: {
        newFileData: {
            type: Object as PropType<INewFileData>,
        },
        newElementFiles: {
            type: Object as PropType<INewFileData>,
        },
        newData: {
            type: Object as PropType<IPostInner>
        },
        uploadProgress: {
            type: Number
        }
    },
    setup() {
        const keyToWord = {
            images: 'Изображения',
            videos_native: 'Загруженные видео',
            documentation: 'Дополнительные документы'
        }

        return {
            keyToWord,
            blockTitle: computed(() => (title: string) => keyToWord[title as keyof IKeyToWord])
        }
    }
})
</script>
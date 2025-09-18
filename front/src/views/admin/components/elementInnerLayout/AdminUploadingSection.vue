<template>
<div class="admin-element-inner__field"
     v-if="newFileData">
    <div class="admin-element-inner__fields"
         v-for="itemKey in Object.keys(newFileData)"
         :key="'key' + itemKey">
        <div v-if="newFileData && itemKey !== 'videos_embed'"
             class="">
            <p class="admin-element-inner__field-title fs-l">{{ blockTitle(itemKey) }} </p>
            <FileUploader @upload="(e) => $emit('handleUpload', e)"
                          @reloadData="$emit('reloadData')"
                          :uploadType="(itemKey as keyof IKeyToWord)"
                          :existFiles="(newFileData[itemKey as keyof IKeyToWord])" />
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, type PropType, computed } from 'vue';
import type { INewFileData } from '@/interfaces/IEntities';
import type { IPostInner } from '@/components/tools/common/PostInner.vue';
import FileUploader from '@/components/tools/common/FileUploader.vue';

interface IKeyToWord {
    images: string,
    videos_native: string,
    documentation: string
}

export default defineComponent({
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
    },
    components: {
        FileUploader
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
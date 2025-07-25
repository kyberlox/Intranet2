<template>
    <div class="admin-element-inner__field-content">
        <p class="admin-element-inner__field-title">{{ item?.name }}</p>
        <div class="admin-element-inner__documents">
            <a v-for="(doc, index) in item?.values"
               class="admin-element-inner__document-link"
               :key="index"
               :href="doc"
               target='_blank'>
                {{ doc }}
            </a>
        </div>
        <FileUploader class="admin-element-inner__file-uploader" />
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from 'vue';
import FileUploader from './FileUploader.vue';
import type { IAdminListItem } from '@/interfaces/entities/IAdmin';

export default defineComponent({
    components: {
        FileUploader
    },
    props: {
        item: {
            type: Object as PropType<IAdminListItem>
        }
    },
    setup(props, { emit }) {
        return {

        }
    }
})
</script>
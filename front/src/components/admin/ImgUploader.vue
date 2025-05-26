<template>
    <div class="card">
        <FileUpload name="demo[]"
                    url="/api/upload"
                    @upload="onAdvancedUpload($event)"
                    :multiple="true"
                    accept="image/*"
                    :maxFileSize="1000000">
            <template #empty>
                <span class="drag-n-drop__text">Перетащите изображения в эту область либо загрузите по кнопке</span>
            </template>
        </FileUpload>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    setup() {
        const onAdvancedUpload = () => {
            console.log(11)
        };
        return {
            onAdvancedUpload
        }
    }
})
</script>

<style lang="scss">
.drag-n-drop__wrapper {
    display: block;
    padding: 10px;
    min-height: 250px;
}

.p-fileupload-file-thumbnail {
    flex-grow: 1;
}

.p-badge {
    width: 100%;
}

.p-fileupload-choose-button,
.p-fileupload-upload-button,
.p-fileupload-cancel-button {
    cursor: pointer !important;
}

.p-fileupload-choose-button {
    &:hover {
        color: green !important;
    }
}

.p-fileupload-upload-button {
    &:hover {
        color: orange !important;
    }
}

.p-fileupload-cancel-button {
    &:hover {
        color: red !important;
    }
}

.p-button-danger {
    &:hover {
        color: red !important;
    }

}
</style>
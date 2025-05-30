<template>
    <FileUpload mode="basic"
                name="demo[]"
                url="/api/upload"
                accept="image/*"
                :maxFileSize="1000000"
                @upload="onUpload"
                :auto="true"
                chooseLabel="Добавить" />

</template>

<script lang="ts">
import { ref, defineComponent } from 'vue';

export default defineComponent({
    setup() {
        const fileupload = ref();

        const onUpload = () => {
            fileupload.value.upload();
        };


        return {
            onUpload
        }
    }
})
</script>
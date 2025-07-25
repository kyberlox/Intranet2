<template>
    <div class="admin-element-inner__field-content">
        <p class="admin-element-inner__field-title">{{ item?.name }}</p>
        <div class="admin-element-inner__gallery">
            <div v-for="(itemInner, index) in item?.values"
                 :key="index"
                 class="admin-element-inner__gallery-card">
                <img v-if="typeof itemInner == 'string'"
                     :src="itemInner"
                     class="admin-element-inner__gallery-image"
                     alt="Изображение элемента" />
                <div v-if="typeof itemInner == 'string'"
                     class="admin-element-inner__gallery-actions">
                    <button class="admin-element-inner__gallery-button admin-element-inner__gallery-button--view"
                            @click.prevent="goToImage(itemInner)">
                        <ZoomIcon />
                    </button>
                    <button class="admin-element-inner__gallery-button admin-element-inner__gallery-button--delete"
                            @click.stop.prevent="removeImage(itemInner)">
                        <CloseIcon />
                    </button>
                </div>
            </div>
        </div>
        <ImgUploader class="admin-element-inner__img-uploader" />
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from 'vue';
import CloseIcon from "@/assets/icons/admin/CloseIcon.svg?component";
import ZoomIcon from '@/assets/icons/admin/ZoomIcon.svg?component'
import ImgUploader from './ImgUploader.vue';
import type { IAdminListItem } from '@/interfaces/entities/IAdmin';


export default defineComponent({
    components: {
        ImgUploader,
        CloseIcon,
        ZoomIcon
    },
    props: {
        item: {
            type: Object as PropType<IAdminListItem>
        }
    },
    setup(props, { emit }) {
        const value = ref('');

        const removeImage = (data: string) => {
            console.log(data)
        }

        return {
            value,
            handleValuePick: () => emit('pick', value.value),
            goToImage: (e: string) => window.open(e, '_blank'),
            removeImage

        }
    }
})
</script>
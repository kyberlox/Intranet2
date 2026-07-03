<template>
<div class="row">
    <div class="col-12 col-md-6"
         v-if="item.preview_file_url && !(item.preview_file_url.includes('no-user'))">
        <div class="memo__item__main__img__wrapper">
            <div class="memo__item__main__img"
                 :key="getPreviewPhoto(item)"
                 v-lazy-load="getPreviewPhoto(item)"
                 alt="изображение с памятки">
            </div>
        </div>
    </div>
    <div :class="{
        'col-12 col-md-6': item.preview_file_url && !item.preview_file_url.includes('no-user'),
        'col-12': !item.preview_file_url || item.preview_file_url.includes('no-user')
    }">
        <div class="memo__item__content">
            <div v-if="newMemo"
                 class="news__detail__discr">
                <b>{{ item.name }}</b>
            </div>
            <div class="news__detail__discr"
                 v-html="item.content_text?.replaceAll('&nbsp;', ' ')"></div>
            <div v-if="item.images?.length && item.images.length > 1 && type !== 'ending'"
                 class="news__detail__discr__image__wrapper">
                <img v-for="(image, index) in item.images.slice(1)"
                     :key="index + 'memiImg'"
                     class="news__detail__discr__image"
                     :src="(image as IBXFileType).file_url"
                     alt="изображение с памятки" />
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import type { IBXFileType, IForNewWorker } from "@/interfaces/IEntities";
import { defineComponent, type PropType } from "vue";
import { featureFlags } from "@/assets/static/featureFlags";

export default defineComponent({
    name: "ForNewWorker",
    props: {
        item: {
            type: Object as PropType<IForNewWorker>,
            required: true
        },
        type: {
            type: String,
        },
        officeEnding: {
            type: Boolean,
            default: false
        }
    },
    setup(props) {

        const getPreviewPhoto = (item: IForNewWorker) => {
            if (props.type == 'ending') {
                console.log(item.images)
                return props.officeEnding ? (item.images as IBXFileType[])[0].file_url : (item.images as IBXFileType[])[1].file_url
            } else return item.preview_file_url
        }
        return {
            getPreviewPhoto,
            newMemo: featureFlags.newWorkerMemo
        }
    }
});
</script>

<style lang="css">
.news__detail__discr__image__wrapper {
    text-align: right;
}

.news__detail__discr__image {
    max-width: 250px;
    padding: 10px;
    border: 1px solid rgba(128, 128, 128, 0.378);
    border-radius: 16px;
}
</style>
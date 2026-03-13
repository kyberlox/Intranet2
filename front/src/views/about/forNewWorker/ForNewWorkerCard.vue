<template>
<div class="row">
    <div class="col-12 col-md-6 col-lg-6 col-xl-8"
         v-if="item.preview_file_url && !(item.preview_file_url.includes('no-user'))">
        <div class="memo__item__main__img__wrapper">
            <div class="memo__item__main__img"
                 v-lazy-load="item.preview_file_url"
                 alt="изображение с памятки">
            </div>
        </div>
    </div>
    <div :class="{
        'col-12 col-md-6 col-lg-6 col-xl-4': item.preview_file_url && !item.preview_file_url.includes('no-user'),
        'col-12': !item.preview_file_url || item.preview_file_url.includes('no-user')
    }">
        <div class="memo__item__content">
            <div v-if="newMemo"
                 class="news__detail__discr">
                <b>{{
                    item.name
                    }}</b>
            </div>
            <div class="news__detail__discr"
                 v-html="item.content_text?.replaceAll('&nbsp;', ' ')"></div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import type { IForNewWorker } from "@/interfaces/IEntities";
import { defineComponent, type PropType } from "vue";
import { featureFlags } from "@/assets/static/featureFlags";

export default defineComponent({
    name: "ForNewWorker",
    props: {
        item: {
            type: Object as PropType<IForNewWorker>,
            required: true
        }
    },
    setup() {
        return {
            newMemo: featureFlags.newWorkerMemo
        }
    }
});
</script>

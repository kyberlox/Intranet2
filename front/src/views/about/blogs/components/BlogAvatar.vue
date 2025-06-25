<template>
    <RouterLink :to="{
        name: 'blogOf',
        params: { id: author?.authorId }
    }"
                class="blogs__item col-12 col-md"
                :title="`Блог | ${author?.title}`">
        <div class="blogs__item__img-wrapper">
            <div :style="{ backgroundImage: `url('https://placehold.co/206x206')` }"
                 class="blogs__item__img img-fluid img-thumbnail rounded-circle"></div>
            <!-- <div v-lazy-load="author.indirect_data.preview_photo_url ?? ''"
                 class="blogs__item__img img-fluid img-thumbnail rounded-circle"></div> -->
        </div>
        <div class="blogs__item-text text-center">
            <h3 class="blogs__item-title">
                {{ author?.title }}
            </h3>
        </div>
    </RouterLink>
</template>

<script lang="ts">
import { makeSlashToBr } from "@/utils/StringUtils";
import { defineComponent } from "vue";

export default defineComponent({
    props: {
        author: Object,
        from: {
            type: String,
            default: 'blogs',
        },
    },
    setup(props) {
        return {
            makeSlashToBr,
        };
    },
});
</script>
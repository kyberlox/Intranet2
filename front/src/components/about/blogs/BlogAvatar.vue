<template>
    <RouterLink :to="{ name: 'blogOf', params: { name: author?.href } }"
                class="blogs__item col-12 col-md"
                :title="`Блог | ${author?.title}`">
        <div class="blogs__item__img-wrapper">
            <div :style="{ backgroundImage: `url('https://portal.emk.ru/upload/resize_cache/main/3a9/la6p0xocac50n4ai2i4bmu2pdeeeyyqf/360_360_2/%D0%94%D1%80%D1%83%D0%B7%D0%B8%D0%BD%D0%B0.jpg.png')` }"
                 class="blogs__item__img img-fluid img-thumbnail rounded-circle"></div>
        </div>
        <div class="blogs__item-text text-center">
            <h3 class="blogs__item-title">
                <p>{{ author?.title }}</p>
            </h3>
            <p class="blogs__item-description"
               v-html="makeSlashToBr(author?.description)"></p>
        </div>
    </RouterLink>
</template>

<script lang="ts">
import { makeSlashToBr } from "@/utils/StringUtils";
import { defineComponent } from "vue";
export default defineComponent({
    props: {
        author: Object,
    },
    setup() {
        return {
            makeSlashToBr,
        };
    },
});
</script>

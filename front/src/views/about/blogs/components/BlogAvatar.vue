<template>
    <div class="blogs__avatar-wrapper">
        <RouterLink v-if="author"
                    :to="{
                        name: 'blogOf',
                        params: { id: author?.authorId }
                    }"
                    class="blogs__item col-12 col-md"
                    :title="`Блог | ${author?.title}`">
            <div class="blogs__item__img-wrapper">
                <div v-lazy-load="author?.authorAvatar"
                     class="blogs__item__img img-fluid img-thumbnail rounded-circle"></div>
            </div>
            <div class="blogs__item-text text-center">
                <h3 class="blogs__item-title">
                    {{ author?.title }}
                </h3>
            </div>
        </RouterLink>
        <a v-if="needLink && author?.link"
           class="blogs__item-contact"
           :href=author.link
           target="_blank">
            {{ author.link }}
        </a>
        <img v-if="author?.telegramQr && needLink"
             :src="author?.telegramQr"
             alt="Ссылка на ресурс" />
    </div>
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
        needLink: {
            type: Boolean,
            default: false
        },
    },
    setup() {
        return {
            makeSlashToBr,
        };
    },
});
</script>
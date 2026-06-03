<template>
<div class="blogs__avatar-wrapper">
    <RouterLink v-if="author"
                :to="!noRoute ? {
                    name: 'blogOf',
                    params: { id: author?.authorId }
                } : ''"
                class="blogs__item col-12 col-md"
                :title="`Блог | ${author?.title ?? author?.TITLE}`">
        <div class="blogs__item__img-wrapper">
            <div v-lazy-load="author?.authorAvatar ?? author.photo_file_url"
                 class="blogs__item__img img-fluid  rounded-circle"></div>
        </div>
        <div class="blogs__item-text text-center">
            <div class="blogs__item-title"
                 v-html="formatTitle()"></div>
        </div>
    </RouterLink>
    <!-- <a v-if="needLink && author?.link"
       class="blogs__item-contact"
       :href=author.link
       target="_blank">
        {{ author.link }}
    </a>
    <img v-if="author?.telegramQr && needLink"
         :src="author?.telegramQr"
         alt="Ссылка на ресурс" /> -->
</div>
</template>

<script lang="ts">
import { makeSlashToBr } from "@/utils/stringUtils";
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
        noRoute: {
            type: Boolean,
            default: false
        }
    },
    setup(props) {
        const formatTitle = () => {
            const newTitle = props.author?.authorTitle ?? props.author?.TITLE;
            if (newTitle && newTitle.includes(';')) {
                return `${newTitle.split(';')[0]}<div class="blogs__item-title--small">${newTitle.split(';')[1]}</div>`
            }
            else return props.author?.title
        }
        return {
            makeSlashToBr,
            formatTitle
        };
    },
});
</script>

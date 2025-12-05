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
                 class="blogs__item__img img-fluid  rounded-circle"></div>
        </div>
        <div class="blogs__item-text text-center">
            <div class="blogs__item-title"
                 v-html="formatTitle()"></div>
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
    },
    setup(props) {
        const formatTitle = () => {
            if (props.author?.authorTitle) {
                return `${props.author?.authorTitle.split(';')[0]}<div class="blogs__item-title--small">${props.author?.authorTitle.split(';')[1]}</div>`
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

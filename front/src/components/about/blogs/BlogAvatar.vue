<template>
    <RouterLink v-if="author && author.PROPERTY_444"
                :to="{
                    name: 'blogOf',
                    params: { id: author?.PROPERTY_444.authorId }
                }"
                class="blogs__item col-12 col-md"
                :title="`Блог | ${author?.NAME}`">
        <div class="blogs__item__img-wrapper">
            <div :style="{ backgroundImage: `url('https://placehold.co/206x206')` }"
                 class="blogs__item__img img-fluid img-thumbnail rounded-circle"></div>
        </div>
        <div class="blogs__item-text text-center">
            <h3 class="blogs__item-title">
                Фио
            </h3>
            <p class="blogs__item-description"
               v-html="'sample text'"></p>
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
            required: true,
        },
    },
    setup(props) {
        console.log(props);
        return {
            makeSlashToBr,
        };
    },
});
</script>
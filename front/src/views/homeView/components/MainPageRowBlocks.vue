<template>
    <div v-if="card"
         class="homeview__grid__card col-12 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex flex-column">
        <RouterLink :to="{ name: card.href, params: { id: card.id } }"
                    class="homeview__grid__card__link">
            <span v-if="modifiers?.includes('mixedType')"
                  class="homeview__grid__card__group-title homeview__grid__card__group-title--mixed">
                <span v-if="card.blockTitle">{{ card.blockTitle }}</span>
            </span>
            <div class="homeview__grid__card__image"
                 :style="{ backgroundImage: `url(${card.image ?? 'https://placehold.co/360x206'})` }"></div>
            <div v-if="card.title"
                 class="homeview__grid__card__title homeview__grid__card__title--gallery">{{ card.title }}</div>
            <Reactions v-if="card.reactions"
                       :reactions="card.reactions"
                       :type="'interview'" />
        </RouterLink>
    </div>
</template>

<script lang="ts">
import Reactions from "@/components/tools/common/Reactions.vue";
import { defineComponent } from "vue";
import type { PropType } from "vue";
import type { ImageWithHref, BlockImage } from '@/interfaces/IMainPage'

export default defineComponent({
    components: { Reactions },
    props: {
        card: {
            type: Object as PropType<ImageWithHref | BlockImage>,
            required: true,
        },
        type: {
            type: String,
            default: 'postPreview',
        },
        modifiers: {
            type: Array as PropType<string[]>,
        }
    },
});
</script>

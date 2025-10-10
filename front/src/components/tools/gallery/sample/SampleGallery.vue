<template>
<div v-if="gallery.length"
     class="homeview__grid__gallery">
    <div class="homeview__grid">
        <div v-for="card in gallery"
             :key="'homeCard' + card.id"
             class="homeview__grid__card col-12 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex flex-column">
            <RouterLink :to='{ name: routeTo, params: { id: String((card.id)) } }'
                        class="homeview__grid__card__link">
                <div class="homeview__grid__card__image"
                     v-lazy-load="card.preview_file_url">
                </div>
                <div class="homeview__grid__card__info">
                    <div v-if="card.name"
                         class="homeview__grid__card__title homeview__grid__card__title--gallery"
                         :class="{ 'homeview__grid__card__title--video': type == 'video' }">
                        {{ card.name }}
                    </div>
                </div>
                <Reactions v-if="card.reactions && card.id"
                           :reactions="card.reactions"
                           :id="card.id"
                           :type="type"
                           :modifiers="modifiers"
                           :date="card.date_publiction ?? card.date_creation" />
            </RouterLink>
        </div>
    </div>
</div>
<SampleGallerySkeleton v-else />
</template>


<script lang="ts">
import Reactions from "@/components/tools/common/Reactions.vue";
import { defineComponent, type PropType } from "vue";
import SampleGallerySkeleton from "./SampleGallerySkeleton.vue";
import type { IBaseEntity } from "@/interfaces/IEntities";

export default defineComponent({
    name: 'SampleGallery',
    props: {
        gallery: {
            type: Object as PropType<IBaseEntity[]>,
            required: true,
        },
        type: {
            type: String as PropType<"postPreview" | "blog" | "video" | "interview" | "ourPeople">,
            default: 'gallery',
        },
        routeTo: {
            type: String,
        },
        modifiers: {
            type: Array<string>
        },
        needDate: {
            type: Boolean,
            default: () => false
        }
    },
    components: {
        Reactions,
        SampleGallerySkeleton
    },
    setup() {

        return {
        }
    }
});
</script>
<template>
    <div v-if="gallery.length"
         class="homeview__grid__gallery">
        <div class="homeview__grid">
            <div v-for="card in gallery"
                 :key="'homeCard' + card.id"
                 class="homeview__grid__card col-12 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex flex-column">
                <RouterLink v-if="card.indirect_data && card.indirect_data.ID"
                            :to='{ name: routeTo, params: { id: String((card.indirect_data.ID)) } }'
                            class="homeview__grid__card__link">
                    <div class="homeview__grid__card__image"
                         v-lazy-load="card.preview_file_url">
                    </div>
                    <div class="homeview__grid__card__info">
                        <div v-if="card.name"
                             class="homeview__grid__card__title homeview__grid__card__title--gallery"
                             :class="{ 'homeview__grid__card__title--video': type == 'video' }">{{ card.name }}</div>
                    </div>
                    <Reactions v-if="card.reactions"
                               :reactions="card.reactions"
                               :type="type" />
                </RouterLink>
            </div>
        </div>
    </div>
    <SampleGallerySkeleton v-else />
</template>
<script lang="ts">
import Reactions from "@/components/tools/common/Reactions.vue";
import { defineComponent, type PropType } from "vue";
import { blockRouteTips } from "@/assets/static/sectionTips";
import type { IUnionEntities } from "@/interfaces/IEntities";
import SampleGallerySkeleton from "./SampleGallerySkeleton.vue";

export default defineComponent({
    name: 'SampleGallery',
    props: {
        gallery: {
            type: Object as PropType<IUnionEntities[]>,
            required: true,
        },
        type: {
            type: String,
            default: 'gallery',
        },
        routeTo: {
            type: String,
        },
    },
    components: {
        Reactions,
        SampleGallerySkeleton
    },
    setup(props) {

        return {
            blockRouteTips,
        }
    }
});
</script>

<style lang="scss">
.homeview__grid__card__image {
    &.lazy-loading {
        background-color: #f0f0f0;
        background-image: none !important;
        position: relative;

        &::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg,
                    transparent 0%,
                    rgba(255, 255, 255, 0.4) 50%,
                    transparent 100%);
            animation: shimmer 1.5s infinite;
        }
    }

    &.lazy-loaded {
        animation: fadeIn 0.3s ease-in-out;
    }

    &.lazy-error {
        background-color: #ffebee;
        position: relative;

        &::after {
            content: '⚠️';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 2rem;
            opacity: 0.5;
        }
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}
</style>
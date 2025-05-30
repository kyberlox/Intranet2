<template>
    <div class="homeview__grid__gallery">
        <div class="homeview__grid">
            <div v-for="card in gallery"
                 :key="'homeCard' + card.id"
                 class="homeview__grid__card col-12 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex flex-column">
                <!-- <div class="homeview__grid__card_group-title">{{ card.name }}</div> -->
                <RouterLink v-if="card.indirect_data && card.indirect_data.ID"
                            :to='{ name: routeTo, params: { id: String((card.indirect_data.ID)) } }'
                            class="homeview__grid__card__link">
                    <div v-if="card.indirect_data.PREVIEW_PICTURE"
                         class="homeview__grid__card__image"
                         :style="{ backgroundImage: `url(${card.indirect_data.PREVIEW_PICTURE.includes('https') ? card.indirect_data.PREVIEW_PICTURE : 'https://placehold.co/360x206'})` }">
                    </div>
                    <div v-else-if="card.indirect_data.DETAIL_PICTURE"
                         class="homeview__grid__card__image"
                         :style="{ backgroundImage: `url(${card.indirect_data.DETAIL_PICTURE.includes('https') ? card.indirect_data.DETAIL_PICTURE : 'https://placehold.co/360x206'})` }">
                    </div>
                    <div v-else
                         class="homeview__grid__card__image"
                         :style="{ backgroundImage: `url('https://placehold.co/360x206')` }">
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
</template>
<script lang="ts">
import Reactions from "@/components/Reactions.vue";
import { defineComponent, type PropType } from "vue";
import { blockRouteTips } from "@/assets/staticJsons/sectionTips";
import type { IUnionEntities } from "@/interfaces/IEntities";

export default defineComponent({
    components: { Reactions },
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
        id: {
            type: Number,
        }
    },
    setup() {

        return {
            blockRouteTips
        }
    }
});
</script>
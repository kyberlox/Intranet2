<template>
    <div class="home__view__grid__gallery">
        <div class="home__view__grid">
            <div v-for="card in gallery"
                 :key="'homeCard' + card.id"
                 class="home__view__grid__card col-12 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex flex-column">
                <!-- <div class="home__view__grid__card_group-title">{{ card.name }}</div> -->
                <RouterLink :to="{ name: type !== 'video' ? 'ourPeopleInner' : 'videoInterview', params: { id: card.indirect_data.ID } }"
                            class="home__view__grid__card__link">
                    <div class="home__view__grid__card__image"
                         :style="{ backgroundImage: `url(${card.indirect_data.PREVIEW_PICTURE.includes('https') ? card.PREVIEW_PICTURE : 'https://placehold.co/360x206'})` }">
                    </div>
                    <div class="home__view__grid__card__info">
                        <div v-if="card.name"
                             class="home__view__grid__card__title home__view__grid__card__title--gallery"
                             :class="{ 'home__view__grid__card__title--video': type == 'video' }">{{ card.name }}</div>
                        <div v-if="card.description"
                             class="home__view__grid__card__description">{{ card.description }}</div>
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
import { defineComponent } from "vue";
import { blockRouteTips } from "@/assets/staticJsons/sectionTips";

export default defineComponent({
    components: { Reactions },
    props: {
        gallery: {
            type: Object,
            required: true,
        },
        type: {
            type: String,
            default: 'gallery',
        },
    },
    setup(props) {
        return {
            blockRouteTips
        }
    }
});
</script>
<style>
.home__view__grid__card__info {
    display: flex;
    flex-direction: column;
    gap: 3px;
    justify-content: flex-start;
}
</style>
<template>
    <div class="home__view__grid__gallery">
        <div class="home__view__grid">
            <div v-for="card in gallery"
                 :key="'homeCard' + card.id"
                 class="home__view__grid__card col-12 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex flex-column">
                <div class="home__view__grid__card_group-title">{{ card.name }}</div>
                <RouterLink :to="{ name: type !== 'video' ? card.href : 'videoInterview', params: { id: card.id } }"
                            class="home__view__grid__card__link">
                    <div class="home__view__grid__card__image"
                         :style="{ backgroundImage: `url(${card.image})` }"></div>
                    <div class="home__view__grid__card__info">
                        <div v-if="card.title"
                             class="home__view__grid__card__title home__view__grid__card__title--gallery"
                             :class="{ 'home__view__grid__card__title--video': type == 'video' }">{{ card.title }}</div>
                        <div v-if="card.description"
                             class="home__view__grid__card__description">{{ card.description }}</div>
                    </div>
                    <Reactions :reactions="card.reactions"
                               :type="type" />
                </RouterLink>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import Reactions from "@/components/Reactions.vue";
import { defineComponent } from "vue";

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
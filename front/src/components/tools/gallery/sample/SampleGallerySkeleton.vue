<template>
    <div class="homeview__grid__gallery">
        <div class="homeview__grid">
            <div v-for="n in skeletonCount"
                 :key="'skeleton-grid__gallery' + n"
                 class="homeview__grid__card col-12 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex flex-column">
                <div class="homeview__grid__card__link skeleton-grid__gallery-card">
                    <div class="homeview__grid__card__image skeleton-grid__gallery-image">
                    </div>
                    <div class="homeview__grid__card__info">
                        <div class="homeview__grid__card__title skeleton-grid__gallery-title">
                        </div>
                        <div class="skeleton-grid__gallery-reactions"
                             v-if="reactions == true">
                            <div class="skeleton-grid__gallery-reaction"></div>
                            <div class="skeleton-grid__gallery-reaction"></div>
                            <div class="skeleton-grid__gallery-reaction"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    props: {
        skeletonCount: {
            type: Number,
            default: 15
        },
        reactions: {
            type: Boolean,
            default: true
        }
    }
});
</script>
<template>
    <div class="flexGallery"
         v-if="true">
        <div v-for="n in skeletonCount"
             :key="'skeleton-flex__gallery' + n">
            <div class="flexGallery__card skeleton-flex__gallery-card">
                <div class="flexGallery__card__img-wrapper"
                     :class="{ 'flexGallery__card__img-wrapper--noFullWidthImg': modifiers.includes('noFullWidthImg') }">
                    <div class="flexGallery__card__img skeleton-flex__gallery-image">
                    </div>
                </div>
                <div class="flexGallery__card__title flexGallery__card__title--text-date">
                    <span class="skeleton-flex__gallery-date"></span>
                    <span class="skeleton-flex__gallery-title-text"></span>
                </div>
                <div v-if="modifiers.includes('buttons')"
                     class="flexGallery__card__buttons">
                    <div class="skeleton-flex__gallery-button"></div>
                    <div class="skeleton-flex__gallery-button"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: 'FlexGalleryskeleton-flex__gallery',
    props: {
        skeletonCount: {
            type: Number,
            default: 12
        },
        modifiers: {
            type: Array,
            default: () => ['']
        }
    }
});
</script>
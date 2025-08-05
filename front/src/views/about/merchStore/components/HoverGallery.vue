<template>
    <div class="hover-gallery"
         @mousemove="handleMouseMove"
         @mouseleave="resetToFirstImage">

        <div class="hover-gallery__indicators"
             v-if="showIndicators && images.length > 1">
            <div v-for="(image, index) in images"
                 :key="index"
                 class="hover-gallery__indicator"
                 :class="{ 'active': currentImageIndex === index }">
            </div>
        </div>

        <div class="hover-gallery__image-container">
            <img :src="currentImage"
                 :alt="alt"
                 class="hover-gallery__image" />
        </div>

        <div class="hover-gallery__zones"
             v-if="images.length > 1">
            <div v-for="(image, index) in images"
                 :key="index"
                 class="hover-gallery__zone"
                 :style="{ width: zoneWidth + '%' }"
                 @mouseenter="setCurrentImage(index)">
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, type PropType } from 'vue'

export default defineComponent({
    name: 'HoverImageGallery',
    props: {
        images: {
            type: Array as PropType<string[]>,
            required: true
        },
        alt: {
            type: String,
            default: 'Gallery image'
        },
        showIndicators: {
            type: Boolean,
            default: true
        }
    },
    setup(props) {
        const currentImageIndex = ref(0);

        const currentImage = computed(() => {
            return props.images[currentImageIndex.value] || props.images[0];
        })

        const zoneWidth = computed(() => {
            return props.images.length > 0 ? 100 / props.images.length : 100;
        })

        const setCurrentImage = (index: number) => {
            if (index >= 0 && index < props.images.length) {
                currentImageIndex.value = index;
            }
        }

        const handleMouseMove = (event: MouseEvent) => {
            const target = event?.currentTarget as HTMLElement;
            const rect = target?.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const zoneIndex = Math.floor((x / rect.width) * props.images.length);
            setCurrentImage(zoneIndex);
        }

        const resetToFirstImage = () => {
            currentImageIndex.value = 0;
        }

        return {
            currentImage,
            currentImageIndex,
            zoneWidth,
            setCurrentImage,
            handleMouseMove,
            resetToFirstImage
        }
    }
})
</script>

<style scoped>
.hover-gallery {
    position: relative;
    width: 100%;
    max-width: 300px;
    overflow: hidden;
    text-align: center;
    cursor: pointer;
}

.hover-gallery__image-container {
    /* width: 100%;
    height: 100%;
    position: relative;
    aspect-ratio: 1;
    max-width: 300px;
    max-height: 300px; */
}

.hover-gallery__image {
    width: 100%;
    height: 100%;
    /* max-width: 300px;
    max-height: 300px; */
    object-fit: cover;
    transition: opacity 0.2s ease;
    aspect-ratio: 1;
}

.hover-gallery__zones {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    z-index: 2;
}

.hover-gallery__zone {
    height: 100%;
}

.hover-gallery__indicators {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 5px;
    width: 100%;
    z-index: 3;
    padding: 10px;
    max-width: 90%;
}

.hover-gallery__indicator {
    width: 100%;
    background: #6363639c;
    height: 3px;
}

.hover-gallery__indicator.active {
    background: var(--emk-brand-color);
}
</style>
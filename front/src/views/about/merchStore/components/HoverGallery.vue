<template>
    <div class="hover-gallery"
         @mousemove="handleMouseMove"
         @mouseleave="resetToFirstImage">

        <div class="hover-gallery__indicators"
             v-if="showIndicators">
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

        <div class="hover-gallery__zones">
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
    height: 200px;
    /* Настройте под ваши нужды */
    overflow: hidden;
    cursor: pointer;
}

.hover-gallery__image-container {
    width: 100%;
    height: 100%;
    position: relative;
}

.hover-gallery__image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: opacity 0.2s ease;
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
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 5px;
    z-index: 3;
}

.hover-gallery__indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.5);
    transition: background-color 0.2s ease;
}

.hover-gallery__indicator.active {
    background-color: rgba(255, 255, 255, 1);
}
</style>
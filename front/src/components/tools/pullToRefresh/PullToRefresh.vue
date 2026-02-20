<template>
<div class="pull-to-refresh"
     :class="{ 'pull-to-refresh--refreshing': isRefreshing }"
     @touchstart="handleTouchStart"
     @touchmove="handleTouchMove"
     @touchend="handleTouchEnd">
    <Loader v-if="isRefreshing" />
    <slot></slot>
</div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Loader from '@/components/layout/Loader.vue';

export default defineComponent({
    name: 'PullToRefresh',
    components: {
        Loader
    },
    props: {
        refreshing: {
            type: Boolean,
            default: false
        },
        onRefresh: {
            type: Function,
            required: true
        }
    },
    setup(props) {
        const startY = ref(0);
        const pullDistance = ref(0);
        const isRefreshing = ref(false);
        const isTracking = ref(false);

        const handleTouchStart = (e: TouchEvent) => {
            const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            if (scrollTop === 0) {
                isTracking.value = true;
                startY.value = e.touches[0].clientY;
                pullDistance.value = 0;
            }
        };

        const handleTouchMove = (e: TouchEvent) => {
            if (!isTracking.value) return;

            const currentY = e.touches[0].clientY;
            const distance = currentY - startY.value;

            if (distance > 0) {
                e.preventDefault();
                pullDistance.value = Math.min(distance, 120);
            }
        };

        const handleTouchEnd = () => {
            if (!isTracking.value) return;

            isTracking.value = false;

            if (pullDistance.value > 60 && !isRefreshing.value) {
                isRefreshing.value = true;
                pullDistance.value = 80;

                Promise.resolve((props.onRefresh as () => Promise<void>)())
                    .then(() => {
                        isRefreshing.value = false;
                        pullDistance.value = 0;
                    });
            } else {
                pullDistance.value = 0;
            }
        };

        return {
            pullDistance,
            isRefreshing,
            handleTouchStart,
            handleTouchMove,
            handleTouchEnd
        };
    }
});
</script>
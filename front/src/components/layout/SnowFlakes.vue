<template>
<div class="snowflakes-container" />
</template>

<script lang="ts">
import { defineComponent, onMounted, onUnmounted } from 'vue';

interface Snowflake {
  id: number;
  element: HTMLElement;
  animationFrameId: number;
  startTime: number;
  duration: number;
  horizontalMove: number;
  startLeft: number;
}

export default defineComponent({
  name: 'SnowFlakes',
  setup() {
    let snowflakeCounter = 0;
    const snowflakes = new Map<number, Snowflake>();
    let intervalId: ReturnType<typeof setInterval> | null = null;

    const snowflakeSvg = `<svg width="20" height="20" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--emojione" preserveAspectRatio="xMidYMid meet"><path d="M60.5 30.5h-6.9l4.2-4.2c.6-.6.6-1.5 0-2.1s-1.5-.6-2.1 0l-6.3 6.3h-4.7l2.5-2.5c.6-.6.6-1.5 0-2.1s-1.5-.6-2.1 0l-4.6 4.6h-4.8l9-9h8.9c.8 0 1.5-.7 1.5-1.5s-.7-1.5-1.5-1.5h-5.9l5.5-5.5c.6-.6.6-1.5 0-2.1s-1.5-.6-2.1 0l-5.5 5.5v-5.9C45.5 9.6 44.9 9 44 9s-1.5.7-1.5 1.5v8.9l-9 9v-4.8l4.6-4.6c.6-.6.6-1.5 0-2.1s-1.5-.6-2.1 0l-2.5 2.5v-4.7l6.3-6.3c.6-.6.6-1.5 0-2.1s-1.5-.6-2.1 0l-4.2 4.2v-7c0-.8-.7-1.5-1.5-1.5s-1.5.7-1.5 1.5v6.9l-4.2-4.2c-.6-.6-1.5-.6-2.1 0s-.6 1.5 0 2.1l6.3 6.3v4.7L28 16.8c-.6-.6-1.5-.6-2.1 0s-.6 1.5 0 2.1l4.6 4.6v4.8l-9-9v-8.9c0-.8-.7-1.4-1.5-1.4s-1.5.7-1.5 1.5v5.9L13 10.9c-.6-.6-1.5-.6-2.1 0s-.6 1.5 0 2.1l5.5 5.5h-5.9c-.9 0-1.5.6-1.5 1.5s.7 1.5 1.5 1.5h8.9l9 9h-4.8L19 25.9c-.6-.6-1.5-.6-2.1 0s-.6 1.5 0 2.1l2.5 2.5h-4.7l-6.3-6.3c-.6-.6-1.5-.6-2.1 0s-.6 1.5 0 2.1l4.2 4.2h-7c-.8 0-1.5.7-1.5 1.5s.7 1.5 1.5 1.5h6.9l-4.2 4.2c-.6.6-.6 1.5 0 2.1c.3.3.7.4 1.1.4s.8-.1 1.1-.4l6.3-6.3h4.7L16.8 36c-.6.6-.6 1.5 0 2.1c.3.3.7.4 1.1.4s.8-.1 1.1-.4l4.6-4.6h4.8l-9 9h-8.9c-.9 0-1.5.7-1.5 1.5s.7 1.5 1.5 1.5h5.9L10.9 51c-.6.6-.6 1.5 0 2.1c.3.3.7.4 1.1.4s.8-.1 1.1-.4l5.5-5.5v5.9c0 .8.7 1.5 1.5 1.5s1.5-.7 1.5-1.5v-8.9l9-9v4.8L25.9 45c-.6.6-.6 1.5 0 2.1c.3.3.7.4 1.1.4s.8-.1 1.1-.4l2.5-2.5v4.7l-6.3 6.3c-.6.6-.6 1.5 0 2.1c.3.3.7.4 1.1.4s.8-.1 1.1-.4l4.2-4.2v6.9c0 .8.7 1.5 1.5 1.5s1.5-.7 1.5-1.5v-6.9l4.2 4.2c.3.3.7.4 1.1.4s.8-.1 1.1-.4c.6-.6.6-1.5 0-2.1l-6.3-6.3v-4.7l2.5 2.5c.3.3.7.4 1.1.4s.8-.1 1.1-.4c.6-.6.6-1.5 0-2.1l-4.6-4.6v-4.8l9 9v8.9c0 .8.7 1.5 1.5 1.5s1.5-.7 1.5-1.5v-5.9l5.5 5.5c.3.3.7.4 1.1.4s.8-.1 1.1-.4c.6-.6.6-1.5 0-2.1l-5.5-5.5H54c.8 0 1.5-.7 1.5-1.5s-.7-1.5-1.5-1.5h-8.9l-9-9h4.8l4.6 4.6c.3.3.7.4 1.1.4s.8-.1 1.1-.4c.6-.6.6-1.5 0-2.1l-2.5-2.5h4.7l6.3 6.3c.3.3.7.4 1.1.4s.8-.1 1.1-.4c.6-.6.6-1.5 0-2.1l-4.2-4.2h6.9c.8 0 1.5-.7 1.5-1.5s-1.3-1.5-2.1-1.5" fill="#75d6ff"></path></svg>`;

    const injectStyles = () => {
      const styleSheet = document.createElement('style');
      styleSheet.textContent = `
        @keyframes snowflakeWobble {
          0% { transform: translateX(0px) rotate(0deg); }
          50% { transform: translateX(5px) rotate(180deg); }
          100% { transform: translateX(0px) rotate(360deg); }
        }
        
        .snowflake {
          position: fixed;
          pointer-events: none;
          animation: snowflakeWobble 3s linear infinite;
        }
      `;
      document.head.appendChild(styleSheet);
    };

    const createSnowflake = () => {
      const id = snowflakeCounter++;
      const element = document.createElement('div');
      element.className = 'snowflake';
      element.innerHTML = snowflakeSvg;

      const startLeft = Math.random() * window.innerWidth;
      const opacity = Math.random() * 0.7 + 0.3;
      const scale = Math.random() * 0.5 + 0.5;
      const duration = Math.random() * 8000 + 5000;
      const horizontalMove = Math.random() * 200 - 100;

      element.style.left = `${startLeft}px`;
      element.style.top = '-30px';
      element.style.opacity = `${opacity}`;
      element.style.transform = `scale(${scale})`;
      element.style.zIndex = '9999';

      document.body.appendChild(element);

      const snowflake: Snowflake = {
        id,
        element,
        animationFrameId: 0,
        startTime: performance.now(),
        duration,
        horizontalMove,
        startLeft
      };

      snowflakes.set(id, snowflake);

      const animate = (currentTime: number) => {
        const elapsed = currentTime - snowflake.startTime;
        const progress = elapsed / duration;

        if (progress >= 1) {
          element.remove();
          snowflakes.delete(id);
          return;
        }

        const currentTop = -30 + (window.innerHeight + 60) * progress;
        const currentLeft = startLeft + horizontalMove * progress;

        element.style.top = `${currentTop}px`;
        element.style.left = `${currentLeft}px`;

        snowflake.animationFrameId = requestAnimationFrame(animate);
      };

      snowflake.animationFrameId = requestAnimationFrame(animate);
    };

    onMounted(() => {
      injectStyles();
      intervalId = setInterval(createSnowflake, 600);
    });

    onUnmounted(() => {
      if (intervalId) {
        clearInterval(intervalId);
      }

      snowflakes.forEach((snowflake) => {
        cancelAnimationFrame(snowflake.animationFrameId);
        snowflake.element.remove();
      });

      snowflakes.clear();
    });

    return {};
  }
});
</script>

<style scoped>
.snowflakes-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9998;
}
</style>

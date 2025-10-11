<template>
  <div
    ref="arrowElement"
    class="layout__scroll-arrow"
    :class="arrowClass"
    @click="handleArrowClick"
  >
    <ScrollArrowDown class="scroll-arrow"/>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted } from "vue";
import ScrollArrowDown from '@/assets/icons/common/ScrollArrowDown.svg?component';

export default defineComponent({
  name: 'ScrollArrow',
  components: {
    ScrollArrowDown
  },
  setup() {
    const isAtBottom = ref(false);
    const arrowClass = ref('');
    const arrowElement = ref<HTMLElement | null>(null);
    const isVisible = ref(true);

    const handleArrowClick = () => {
      if (isAtBottom.value) {
        const headerElement = document.querySelector('#main-content');
        if (headerElement) {
          headerElement.scrollIntoView({ behavior: 'smooth' });
        } else {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      } else {
        const currentScroll = document.documentElement.scrollTop;
        const viewportHeight = window.innerHeight;
        window.scrollTo({
          top: currentScroll + viewportHeight,
          behavior: 'smooth'
        });
      }
    };

    const checkScrollPosition = () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;

      const nearBottom = scrollTop + windowHeight + 100 >= documentHeight;

      if (nearBottom && !isAtBottom.value) {
        isAtBottom.value = true;
        arrowClass.value = 'layout__scroll-arrow--rotateUp';
      } else if (scrollTop < 100 && isAtBottom.value) {
        isAtBottom.value = false;
        arrowClass.value = 'layout__scroll-arrow--rotateDown';
      }
    };

    const checkArrowVisibility = () => {
      if (!arrowElement.value) return;

      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;

      if (windowHeight >= documentHeight || window.innerWidth < 768) {
        arrowElement.value.style.display = 'none';
        isVisible.value = false;
      } else {
        arrowElement.value.style.display = 'flex';
        isVisible.value = true;
      }
    };

    const onScroll = () => {
      checkScrollPosition();
    };

    const onResize = () => {
      checkArrowVisibility();
      checkScrollPosition();
    };

    onMounted(() => {
      checkArrowVisibility();
      checkScrollPosition();

      window.addEventListener('scroll', onScroll);
      window.addEventListener('resize', onResize);
    });

    onUnmounted(() => {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onResize);
    });

    return {
      arrowClass,
      arrowElement,
      handleArrowClick
    };
  }
});
</script>

<style lang="scss">
@keyframes rotateUp {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(180deg);
  }
}

@keyframes rotateDown {
  from {
    transform: rotate(180deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.layout__scroll-arrow {
  cursor: pointer;
  transition: 0.2s ease;
  border-radius: 100%;
  border: 1px solid #f5821f;
  font-family: Arial, Helvetica, sans-serif;
  position: fixed;
  z-index: 100;
  right: 20px;
  bottom: 20px;
  font-size: 30px;
  width: calc(2.1 * 30px);
  margin: 30px;
  height: calc(2.1 * 30px);
  line-height: calc(2.1 * 30px);
  color: black;
  text-align: center;
  box-sizing: border-box;
  background-color: #ffffffba;
  display: flex;
  justify-content: center;
  align-items: center;

  &>svg{
    width: 30px;
  }

  &--rotateUp {
    animation: rotateUp 1s ease;
    transform: rotate(180deg);
  }

  &--rotateDown {
    animation: rotateDown 1s ease;
    transform: rotate(360deg);
  }

  &:hover {
    color: #f5821f;
    background-color: #ffffffff;
  }
}
</style>

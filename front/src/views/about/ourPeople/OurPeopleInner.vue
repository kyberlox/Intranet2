<template>
  <Interview v-if="interviewFromOurPeople" :interviewInner="interviewFromOurPeople" />
</template>
<script lang="ts">
import Interview from "./components/Interview.vue";
import { defineComponent, onMounted, onUnmounted, ref } from "vue";
import Api from "@/utils/Api";

export default defineComponent({
  components: {
    Interview,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const abortController = new AbortController();
    const interviewFromOurPeople = ref();
    onMounted(async () => {
      const data = await Api.get(
        `article/find_by_ID/${props.id}`,
        null,
        abortController.signal
      );
      interviewFromOurPeople.value = data;
    });

    onUnmounted(() => abortController.abort());

    return {
      interviewFromOurPeople,
    };
  },
});
</script>

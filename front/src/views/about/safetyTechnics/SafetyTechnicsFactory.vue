<template>
    <div class="excursions__training__page mt20">
        <div class="page__title">Посещение производсвенных площадок</div>
        <PostInner :previewElement="safetyTechnicsFactoryInner.content" />
    </div>
</template>

<script lang="ts">
import PostInner from "@/components/tools/common/PostInner.vue";
import { defineComponent, ref } from "vue";
import { safetyTechnicsFactoryInner } from "@/assets/static/safetyTechnics";
export default defineComponent({
    components: {
        PostInner,
    },
    setup() {
        const activeIndexInModal = ref(null);
        return {
            activeIndexInModal,
            safetyTechnicsFactoryInner
        };
    },
});
</script>

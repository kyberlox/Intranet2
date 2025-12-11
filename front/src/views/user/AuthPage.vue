<template>
<div class="portal__auth">
    <div class="portal__auth__bg"></div>
    <div class="portal__auth__content">
        <div class="portal__auth__message"> </div>
        <div class="portal__auth__form__auth">
            <Loader class="pos-rel" />
        </div>
    </div>
</div>
</template>
<script lang="ts">
import { useUserData } from '@/stores/userData';
import { defineComponent, onMounted, ref, watch, computed } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import { prefetchSection } from '@/composables/usePrefetchSection';
import Loader from '@/components/layout/Loader.vue';
import { useRoute, useRouter } from 'vue-router';

export default defineComponent({
    name: 'AuthPage',
    components: {
        Loader
    },
    setup() {
        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);
        const isLoading = ref(false);
        const route = useRoute();
        const authKey = computed(() => useUserData().getAuthKey);

        watch((authKey), (newVal) => {
            console.log(newVal);
            if (newVal) {
                if (useUserData().getMyId !== 0) {
                    useUserData().setLogin(true);
                    // prefetchSection('user');
                    isLoading.value = false;
                }
            }
        }, { deep: true, immediate: true })

        return {
            isLoading,
        };
    },
})
</script>
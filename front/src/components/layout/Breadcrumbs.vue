<template>
    <div class="col-12"
         v-if="breadcrumbs && isVisible">
        <div class="breadcrumb">
            <div v-for="(breadcrumb, index) in breadcrumbs"
                 :key="'bread' + index"
                 class="breadcrumb-item">
                <RouterLink :to="{ name: breadcrumb.route }">
                    <span class="breadcrumb-item__title">{{ breadcrumb.title }}</span>
                </RouterLink>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref, type ComputedRef } from 'vue';
import { useRoute } from 'vue-router';
import { watch } from 'vue';

interface IBreadcrumb {
    title: string,
    route: string
}

export default defineComponent({
    setup() {
        const route = useRoute();

        const breadcrumbs: ComputedRef<IBreadcrumb[]> = computed(() =>
            route.meta?.breadcrumbs ? route.meta.breadcrumbs as IBreadcrumb[] : [{ title: 'Назад', route: 'home' }])

        const isVisible = ref(false);

        watch((route), (newVal) => {
            isVisible.value = newVal.name !== 'home';
        }, { immediate: true })

        return {
            breadcrumbs,
            route,
            isVisible
        }
    }
})
</script>
<template>
    <div class="col-12">
        <div class="bx-breadcrumb">
            <div v-for="(breadcrumb, index) in breadcrumbs"
                 :key="'bread' + index"
                 class="bx-breadcrumb-item">
                <RouterLink :to="{ name: breadcrumb.route }"
                            href="/intranet/"
                            title="Главная"
                            itemprop="item">
                    <span>{{ breadcrumb.title }}</span>
                </RouterLink>
            </div>
            <div style="clear:both"></div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

interface IBreadcrumb {
    title: string,
    route: string
}

export default defineComponent({
    props: {
        breadcrumbs: {
            type: Array<IBreadcrumb>
        }
    },
    setup() {
        return {

        }
    }
})
</script>
<template>
    <div class="factory-reports__page mt20">
        <div class="page__title">Репортаж </div>
        <div class="factory-reports">
            <div v-for="item in factoryReports"
                 :key="'report' + item.id"
                 class="factory-reports__report">
                <iframe v-if="item.link"
                        :src="String(repairVideoUrl(item.link))"
                        allowfullscreen></iframe>
                <p>{{ item.name }}</p>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";
import { repairVideoUrl } from "@/utils/embedVideoUtil";
export default defineComponent({
    props: {
        id: {
            type: String,
            required: true,
        },
    },
    setup(props) {
        const factoryGuidData = useFactoryGuidDataStore();
        const factoryReports = computed(() => factoryGuidData.getFactoryReports(Number(props.id)));

        return {
            factoryReports,
            repairVideoUrl
        };
    },
});
</script>
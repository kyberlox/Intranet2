<template>
<LayoutNewsPreview :tagId="tagId"
                   :needTags="true"
                   :pageTitle="pageTitle"
                   :storeItemsName="storeItemsName"
                   :sectionId="Number(sectionId)"
                   :type="'video'"
                   :routeTo="'videoReport'" />
</template>
<script lang="ts">
import { sectionTips } from '@/assets/static/sectionTips';
import { defineComponent } from 'vue';
import LayoutNewsPreview from '@/components/layout/newsPreview/LayoutNewsPreview.vue';
import type { DataState } from '@/stores/viewsData';

export default defineComponent({
    components: {
        LayoutNewsPreview,
    },
    props: {
        tagId: {
            type: String
        }
    },
    setup() {

        return {
            pageTitle: 'Видеорепортажи',
            sectionId: sectionTips['Видеорепортажи'],
            storeItemsName: 'videoReportsData' as keyof DataState
        };
    },
});
</script>

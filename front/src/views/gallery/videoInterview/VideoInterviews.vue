<template>
<LayoutNewsPreview :tagId="tagId"
                   :needTags="false"
                   :pageTitle="pageTitle"
                   :storeItemsName="storeItemsName"
                   :sectionId="Number(sectionId)"
                   :type="'video'"
                   :routeTo="'videoInterview'" />
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
            pageTitle: 'Видеоинтервью',
            sectionId: sectionTips['Видеоинтервью'],
            storeItemsName: 'videoInterviewsData' as keyof DataState
        };
    },
});
</script>

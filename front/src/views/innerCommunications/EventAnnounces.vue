<template>
<LayoutGalleryPreview :pageTitle="pageTitle"
                      :storeItemsName="storeItemsName"
                      :sectionId="Number(sectionId)"
                      :tagId="tagId"
                      :needTags="false"
                      :routeTo="'eventAnnounce'"
                      :needYears="false" />
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { sectionTips } from '@/assets/static/sectionTips';
import LayoutGalleryPreview from '@/components/layout/newsPreview/LayoutGalleryPreview.vue';
import { type DataState } from '@/stores/viewsData';

export default defineComponent({
    components: {
        LayoutGalleryPreview
    },
    props: {
        tagId: {
            type: String
        },
    },
    setup() {
        return {
            pageTitle: 'Афиша',
            sectionId: sectionTips['Афиша'],
            storeItemsName: 'corpLifeData' as keyof DataState
        };
    },
});
</script>
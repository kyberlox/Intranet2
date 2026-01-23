<template>
<LayoutGalleryPreview :pageTitle="pageTitle"
                      :storeItemsName="storeItemsName"
                      :sectionId="Number(sectionId)"
                      :tagId="tagId"
                      :needTags="true"
                      :routeTo="'corpLifeItem'"
                      :needYears="true" />
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
            pageTitle: 'Корпоративная жизнь в фото',
            sectionId: sectionTips['КорпоративнаяЖизнь'],
            storeItemsName: 'corpLifeData' as keyof DataState
        };
    },
});
</script>
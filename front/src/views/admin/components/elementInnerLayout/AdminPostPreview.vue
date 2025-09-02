<template>
    <div v-if="newFileData && sectionId"
         class="admin-element-inner__preview"
         :class="[{ 'admin-element-inner__preview--full-width': previewFullWidth || isMobileScreen },
        { 'admin-element-inner__preview--overflow': sectionId == '15' }]">
        <div v-if="!noPreview">
            <Transition name="layout-change"
                        mode="out-in">
                <LayoutTop v-if="previewFullWidth && !isMobileScreen"
                           class="admin-element-inner__layout-toggle admin-element-inner__layout-toggle--zoom"
                           @click="$emit('changePreviewWidth')" />
                <LayoutLeft v-else-if="!isMobileScreen"
                            class="admin-element-inner__layout-toggle admin-element-inner__layout-toggle--zoom"
                            @click="$emit('changePreviewWidth')" />
            </Transition>
        </div>

        <section class="admin-element-inner__preview-section">
            <PostInner v-if="PreviewTypes['news'].includes(sectionId)"
                       class="admin-element-inner__preview-content mt30"
                       :previewElement="newData"
                       :previewImages="previewImages"
                       :type="'adminPreview'" />
            <Interview v-else-if="PreviewTypes['interview'].includes(sectionId)"
                       class="admin-element-inner__preview-content"
                       :interviewInner="(newData as Record<string, any>)" />
            <CertainBlog v-else-if="PreviewTypes['blogs'].includes(sectionId)"
                         class="admin-element-inner__preview-content"
                         :previewPost="newData"
                         :authorId="String(blogStore.getAuthorByBlogId(String(newId)))" />
        </section>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch, type PropType } from 'vue';
import PostInner from '@/components/tools/common/PostInner.vue';
import Interview from '@/views/about/ourPeople/components/Interview.vue';
import CertainBlog from '@/views/about/blogs/CertainBlog.vue';
import type { IPostInner } from '@/components/tools/common/PostInner.vue';
import type { INewFileData } from '@/interfaces/entities/IAdmin';
import LayoutLeft from "@/assets/icons/admin/LayoutLeft.svg?component";
import LayoutTop from "@/assets/icons/admin/LayoutTop.svg?component";
import { useblogDataStore } from '@/stores/blogData';

export default defineComponent({
    name: 'AdminPostPreview',
    props: {
        previewFullWidth: {
            type: Boolean
        },
        isMobileScreen: {
            type: Boolean
        },
        newFileData: {
            type: Object as PropType<INewFileData>
        },
        newData: {
            type: Object as PropType<IPostInner>
        },
        activeType: {
            type: String as PropType<'noPreview' | 'news' | 'interview' | 'blogs'>
        },
        currentItem: {
            type: Object as PropType<IPostInner>
        },
        sectionId: {
            type: String
        },
        newId: {
            type: String
        }
    },
    components: {
        PostInner,
        Interview,
        CertainBlog,
        LayoutLeft,
        LayoutTop
    },
    setup(props, { emit }) {
        const blogStore = useblogDataStore();
        const noPreview = ref(false);
        const previewImages = ref<string[]>([]);
        const PreviewTypes = {
            'news': ['31', '53', '51', '32', '54'],
            'blogs': ['15'],
            'interview': ['13']
        }

        onMounted(() => {
            const hasPreview = Object.values(PreviewTypes)
                .some(array => array.includes(String(props.sectionId)));

            if (!hasPreview) {
                noPreview.value = true;
                emit('noPreview');
            }
        })

        watch((props), () => {
            if (props.newFileData?.images?.length) {
                props.newFileData?.images?.map((e) => {
                    if (!e.file_url) return
                    previewImages.value.push(e.file_url)
                })
            }
        }, { once: true })

        return {
            PreviewTypes,
            blogStore,
            noPreview,
            previewImages
        }
    }
})
</script>

<template>
    <div class="post-inner__page__wrapper mt20">
        <div v-if="currentPost && (type == 'default' || type == 'adminPreview')"
             class="row">
            <div class="col-12 col-lg-6 mb-2">
                <SwiperBlank :videosNative="currentPost?.videos_native"
                             :videosEmbed="currentPost?.videos_embed"
                             :images="currentPost?.images ? currentPost.images : undefined"
                             :sectionId="currentPost?.section_id" />
            </div>
            <div class="col-12 col-lg-6">
                <div class="news__detail__content">
                    <div v-if="currentPost.name"
                         class="news__detail__top">
                        <div class="row mb-2">
                            <div class="col-12">
                                <h2 class="news__detail__title">
                                    {{ currentPost.name }}
                                </h2>
                            </div>
                        </div>
                    </div>
                    <div class="news__detail">
                        <span v-if="currentPost.date_publiction"
                              class="news__detail__date">{{ currentPost.date_publiction
                            }}</span>
                        <div v-if="currentPost.reactions"
                             class="news__detail__like-wrapper">
                            <Reactions :id="Number(currentPost.id)"
                                       :reactions="currentPost.reactions"
                                       :type="'postPreview'" />
                        </div>
                    </div>
                    <div v-if="currentPost.tags"
                         class="tags"></div>
                    <div v-if="currentPost.indirect_data?.phone_number"
                         class="news__detail__phone-care">
                        Телефон организатора:
                        <br />
                        {{ currentPost.indirect_data?.phone_number }}
                    </div>
                    <div v-if="currentPost.content_text"
                         class="news__detail__discr"
                         v-html="currentPost.content_text"></div>
                    <div v-if="currentPost.documentation"
                         class="news__detail__documents">
                        <div class="news__detail__document"
                             v-for="(doc, index) in currentPost.documentation"
                             :key="'doc' + index">
                            <a class="news__detail__document__link"
                               :href="String(doc.file_url)"
                               _blank>Открыть {{ doc.original_name }}
                                <DocIcon />
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <ComplexGallery v-else-if="type !== 'adminPreview'"
                        :slides="[{ id: 1, images: currentPost?.images }]"
                        :modifiers="['noRoute']" />
    </div>
</template>


<script lang="ts">
import SwiperBlank from "@/components/tools/swiper/SwiperBlank.vue";
import LikeIcon from "@/assets/icons/posts/LikeIcon.svg?component";
import DocIcon from "@/assets/icons/posts/DocIcon.svg?component";
import { defineComponent, type Ref, ref, type PropType, watch } from "vue";
import type { IBaseEntity } from "@/interfaces/IEntities";
import Api from "@/utils/Api";
import ComplexGallery from "../gallery/complex/ComplexGallery.vue";
import Reactions from "./Reactions.vue";
import { parseMarkdown } from "@/utils/useMarkdown";

export interface IPostInner extends IBaseEntity {
    indirect_data?: {
        // Благотв
        organizer?: string,
        phone_number?: string
        // Афиша 
        date_from?: string,
        date_to?: string,
    }
}

export default defineComponent({
    name: 'PostInner',
    components: {
        SwiperBlank,
        LikeIcon,
        DocIcon,
        ComplexGallery,
        Reactions
    },
    props: {
        id: {
            type: String || undefined,
        },
        type: {
            type: String,
            default: 'default'
        },
        previewElement: {
            type: (Object as PropType<IPostInner>) || null
        }
    },
    setup(props) {
        const currentPost = ref<IPostInner>();
        watch((props), () => {
            if ((props.type == 'adminPreview' && props.previewElement) || !props.id) {
                if (props.previewElement == null) {
                    currentPost.value = undefined;
                }
                else currentPost.value = props.previewElement
            }
            else
                Api.get(`article/find_by_ID/${props.id}`)
                    .then((res) => {
                        currentPost.value = res;
                        if (!currentPost.value) return;
                        changeToPostStandart(currentPost as Ref<IPostInner>, res);
                    })
        }, { immediate: true, deep: true })

        const changeToPostStandart = (target: Ref<IPostInner>) => {
            if (target.value == undefined) return;
            if (target.value.section_id == 52) {
                target.value.content_text = target.value.indirect_data?.date_from + ' - ' + target.value.indirect_data?.date_to;
            }

            return target
        }

        return {
            currentPost,
            parseMarkdown
        }
    },
})
</script>
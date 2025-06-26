<template>
    <div class="post-inner__page__wrapper mt20">
        <div v-if="currentPost && (type == 'default' || type == 'adminPreview')"
             class="row">
            <div class="col-12 col-lg-6 mb-2">
                <SwiperBlank :videos="currentPost?.videos ? currentPost.videos : undefined"
                             :images="currentPost?.images ? currentPost.images : undefined"
                             :sectionId="currentPost?.section_id" />
            </div>
            <div v-if="type !== 'onlyImg'"
                 class="col-12 col-lg-6">
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
                              class="news__detail__date">{{ currentPost.date_publiction }}</span>
                        <div v-if="currentPost.reactions"
                             class="news__detail__like-wrapper">
                            <LikeIcon class="news__detail__like-icon" />
                            <span v-if="currentPost.reactions.likes"
                                  class="news__detail__like-count"> {{ currentPost.reactions.likes.count }}</span>
                        </div>
                    </div>
                    <div v-if="currentPost.tags"
                         class="tags"></div>
                    <div v-if="getProperty(currentPost, 'PROPERTY_347')"
                         class="news__detail__phone-care">
                        Телефон организатора:
                        <br />
                        {{ getProperty(currentPost, 'PROPERTY_347') }}
                    </div>
                    <div class="news__detail__discr"
                         v-html="currentPost.content_text"></div>
                    <div v-if="currentPost.documentation"
                         class="news__detail__documents">
                        <div class="news__detail__document"
                             v-for="(doc, index) in currentPost.documentation"
                             :key="'doc' + index">
                            <a class="news__detail__document__link"
                               :href="doc"
                               _blank>Открыть {{ doc }}
                                <DocIcon />
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <FlexGallery v-else-if="type !== 'adminPreview'"
                     :slides="[]"
                     :modifiers="['noRoute']" />
    </div>
</template>


<script lang="ts">
import SwiperBlank from "@/components/tools/swiper/SwiperBlank.vue";
import LikeIcon from "@/assets/icons/posts/LikeIcon.svg?component";
import DocIcon from "@/assets/icons/posts/DocIcon.svg?component";
import { defineComponent, type Ref, onMounted, ref, type PropType } from "vue";
import type { IUnionEntities, IAfishaItem, ICareSlide } from "@/interfaces/IEntities";
import Api from "@/utils/Api";
import { getProperty } from "@/utils/getPropertyFirstPos";
import FlexGallery from "../gallery/complex/ComplexGallery.vue";

export default defineComponent({
    components: {
        SwiperBlank,
        LikeIcon,
        DocIcon,
        FlexGallery
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
            type: Object as PropType<IUnionEntities | null>
        }
    },
    setup(props) {
        const currentPost = ref<IUnionEntities>();
        onMounted(() => {
            if ((props.type == 'adminPreview' && props.previewElement) || !props.id) {
                currentPost.value = props.previewElement
            }
            else
                Api.get(`article/find_by_ID/${props.id}`)
                    .then((res) => {
                        currentPost.value = res;
                        if (!currentPost.value) return;
                        changeToPostStandart(currentPost as Ref<IUnionEntities>, res);
                    })
        })

        const changeToPostStandart = (target: Ref<IUnionEntities>, res: IUnionEntities) => {
            if (target.value == undefined) return;
            const property348Text = getProperty(target.value as ICareSlide, 'PROPERTY_348')?.TEXT;
            const property374Text = getProperty(target.value as IAfishaItem, 'PROPERTY_374')?.TEXT;
            if (property348Text) {
                target.value.content_text = property348Text;
            }
            else if (property374Text) {
                target.value.content_text = property374Text;
            }

            if (res.videos_embed || res.videos_native) {
                const embedVideos = res.videos_embed || [];
                const nativeVideos = res.videos_native || [];
                target.value.videos = embedVideos.concat(nativeVideos);
            }
            return target
        }

        return {
            currentPost,
            getProperty,
        }
    },
})
</script>
<template>
    <div class="post-inner__page__wrapper mt20">
        <div v-if="currentPost && (type == 'default' || type == 'adminPreview')"
             class="row">
            <div class="col-12 col-lg-6 mb-2">
                <SwiperBlank :videos="currentPost?.videos ? currentPost.videos : 0"
                             :images="currentPost?.images ? currentPost.images : ['https://placehold.co/360x206']"
                             :type="'postInner'" />
            </div>
            <div class="col-12 col-lg-6">
                <div class="news__detail__content">
                    <div v-if="currentPost.name || currentPost.indirect_data?.NAME"
                         class="news__detail__top">
                        <div class="row mb-2">
                            <div class="col-12">
                                <h2 class="news__detail__title">{{ currentPost.name || currentPost.indirect_data?.NAME
                                    }}
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
                    <div v-if="currentPost.documents"
                         class="news__detail__documents">
                        <div class="news__detail__document"
                             v-for="(doc, index) in currentPost.documents"
                             :key="'doc' + index">
                            <!-- <a class="news__detail__document__link"
                               :href="doc.link"
                               _blank>Открыть {{ doc.name }}
                                <DocIcon />
                            </a> -->
                        </div>
                    </div>
                    <!-- <div v-if="page == 'news'"
                         class="col-12 news__detail__content__back-to-news">
                        <a href="/intranet/company-life/news/"
                           class="section__item__link">
                            Посмотреть другие новости
                            <span style="display: none">К списку новостей</span>
                        </a>
                    </div> -->
                </div>
            </div>
        </div>
        <FlexGallery v-else-if="type !== 'adminPreview'"
                     :slides="['dss']"
                     :modifiers="['noRoute']" />
    </div>
</template>
<script lang="ts">
import SwiperBlank from "@/components/tools/swiper/SwiperBlank.vue";
import LikeIcon from "@/assets/icons/posts/LikeIcon.svg?component";
import DocIcon from "@/assets/icons/posts/DocIcon.svg?component";
import { defineComponent, type Ref, onMounted, ref } from "vue";
import type { IActualNews, ICareSlide } from "@/interfaces/IEntities";
import Api from "@/utils/Api";
import { getProperty } from "@/utils/getPropertyFirstPos";
import FlexGallery from "./tools/gallery/FlexGallery.vue";
export default defineComponent({
    components: {
        SwiperBlank,
        LikeIcon,
        DocIcon,
        FlexGallery
    },
    props: {
        id: {
            type: String,
        },
        type: {
            type: String,
            default: 'default'
        },
        previewElement: {
            type: Object
        }
    },
    setup(props) {
        const currentPost = ref<IActualNews | ICareSlide>();
        onMounted(() => {
            if (props.type == 'adminPreview') {
                currentPost.value = props.previewElement
            }
            else
                Api.get(`article/find_by_ID/${props.id}`)
                    .then((res) => {
                        currentPost.value = res;
                        if (!currentPost.value) return;
                        changeToPostStandart(currentPost, res);
                    })
        })

        const changeToPostStandart = (target: Ref<IActualNews | ICareSlide | undefined>, res: IActualNews | ICareSlide) => {
            if (target.value == undefined) return;
            const property348Text = getProperty(target.value, 'PROPERTY_348')?.TEXT;
            const property374Text = getProperty(target.value, 'PROPERTY_374')?.TEXT;
            if (property348Text) {
                target.value.content_text = property348Text;
            }
            else if (property374Text) {
                target.value.content_text = property374Text;
            }

            if (!res.embedVideos || !res.nativeVideos) return;
            (target.value as any).videos = res.embedVideos.concat(res.nativeVideos);
        }

        return {
            currentPost,
            getProperty,
        }
    },
})
</script>
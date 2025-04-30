<template>
    <div class="post-inner__page__wrapper mt20">
        <div class="row">
            <div class="col-12 col-lg-6">
                <SwiperBlank :videos="post.videos"
                             :images="post.images ? post.images : ['https://placehold.co/360x206']"
                             :type="'postInner'" />
            </div>

            <div class="col-12 col-lg-6">
                <div class="news__detail__content">
                    <div v-if="post.content_text"
                         class="news__detail__top">
                        <div class="row mb-2">
                            <div class="col-12">
                                <h2 class="news__detail__title mb-2">{{ post.indirect_data?.NAME }}</h2>
                            </div>
                        </div>
                    </div>
                    <div class="news__detail">
                        <span v-if="post.date_publiction"
                              class="news__detail__date">{{ post.date_publiction }}</span>
                        <div v-if="post.reactions"
                             class="news__detail__like-wrapper">
                            <LikeIcon class="news__detail__like-icon" />
                            <span v-if="post.reactions.likes"
                                  class="news__detail__like-count"> {{ post.reactions.likes.count }}</span>
                        </div>
                    </div>
                    <div v-if="post.tags"
                         class="tags"></div>
                    <div class="news__detail__discr"
                         v-html="post.content_text"></div>
                    <div v-if="post.documents"
                         class="news__detail__documents">
                        <div class="news__detail__document"
                             v-for="(doc, index) in post.documents"
                             :key="'doc' + index">
                            <a class="news__detail__document__link"
                               :href="doc.link"
                               _blank>Открыть {{ doc.name }}
                                <DocIcon />
                            </a>
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
    </div>
</template>
<script lang="ts">
import SwiperBlank from "@/components/tools/swiper/SwiperBlank.vue";
import LikeIcon from "@/assets/icons/posts/LikeIcon.svg?component";
import DocIcon from "@/assets/icons/posts/DocIcon.svg?component";
import { defineComponent, type PropType } from "vue";
import type { IPost } from "@/interfaces/IFeedPost";

export default defineComponent({
    components: {
        SwiperBlank,
        LikeIcon,
        DocIcon,
    },
    props: {
        page: {
            type: String,
            default: "news",
        },
        post: {
            type: Object as PropType<IPost>,
            required: true,
        }
    },
    setup() {
        return {

        };
    },
})
</script>
<template>
    <div class="post-inner__page__wrapper mt20">
        <div v-if="currentPost"
             class="row">
            <div class="col-12 col-lg-6 mb-2">
                <SwiperBlank :videos="currentPost.videos"
                             :images="currentPost.images ? currentPost.images : ['https://placehold.co/360x206']"
                             :type="'postInner'" />
            </div>

            <div class="col-12 col-lg-6">
                <div class="news__detail__content">
                    <div v-if="currentPost.indirect_data?.NAME"
                         class="news__detail__top">
                        <div class="row mb-2">
                            <div class="col-12">
                                <h2 class="news__detail__title">{{ currentPost.indirect_data.NAME }}</h2>
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
                    <div v-if="currentPost.indirect_data['PROPERTY_347'] && currentPost.indirect_data['PROPERTY_347'][0]"
                         class="news__detail__phone-care">
                        Телефон организатора:
                        <br />
                        {{ currentPost.indirect_data['PROPERTY_347'][0] }}
                    </div>
                    <div class="news__detail__discr"
                         v-html="currentPost.content_text"></div>
                    <div v-if="currentPost.documents"
                         class="news__detail__documents">
                        <div class="news__detail__document"
                             v-for="(doc, index) in currentPost.documents"
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
import { defineComponent, type PropType, type Ref, onMounted, ref } from "vue";
import type { IActualNews, ICareSlide } from "@/interfaces/INewNews";
import Api from "@/utils/Api";
export default defineComponent({
    components: {
        SwiperBlank,
        LikeIcon,
        DocIcon,
    },
    props: {
        id: {
            type: String,
            required: true,
        }
    },
    setup(props) {
        const currentPost = ref<IActualNews | ICareSlide>();
        onMounted(() => {
            Api.get(`article/find_by_ID/${props.id}`)
                .then((res) => {
                    currentPost.value = res;
                    if (!currentPost.value) return;
                    changeToPostStandart(currentPost, res);
                })
        })

        const changeToPostStandart = (target: Ref<IActualNews | ICareSlide | undefined>, res: IActualNews | ICareSlide) => {
            if (target.value == undefined) return;
            const property348Text = (target.value.indirect_data as any)?.['PROPERTY_348']?.[0]?.["TEXT"];
            const property374Text = (target.value.indirect_data as any)?.['PROPERTY_374']?.[0]?.["TEXT"];
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
        }
    },
})
</script>
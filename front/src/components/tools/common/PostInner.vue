<template>
<div class="news-inner__page__wrapper mt20">
    <div v-if="currentPost && (type == 'default' || type == 'adminPreview')"
         class="row row-gap-50">
        <div v-if="currentPost.section_id !== 32 && sectionId !== '32'"
             class="col-12 col-lg-6 mb-2 pos-rel">
            <SwiperBlank :videosNative="currentPost?.videos_native"
                         :videosEmbed="currentPost?.videos_embed"
                         :images="currentPost?.images ? currentPost.images : previewImages"
                         :sectionId="currentPost?.section_id"
                         :type="'postInner'" />
        </div>
        <div :class="{ 'col-12 col-lg-6': currentPost.section_id !== 32 && sectionId !== '32' }">
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
                <div class="news__detail"
                     :class="{ 'news__detail--corpnews': currentPost.section_id == 32 }">
                    <div v-if="currentPost.reactions"
                         class="news__detail__like-wrapper">
                        <Reactions :id="Number(currentPost.id)"
                                   :reactions="currentPost.reactions"
                                   :type="'postPreview'"
                                   :date="currentPost.date_publiction" />
                    </div>
                </div>
                <div v-if="currentPost.indirect_data && 'tags' in currentPost.indirect_data"
                     class="tags">
                    <div v-for="(tag) in (currentPost.indirect_data.tags as ITag[])"
                         :key="tag.id"
                         class="tag__wrapper ">
                        <div class="tags__tag tags__tag--inner section__item__link btn-air"
                             @click="$emit('pickTag', tag.id)">
                            #{{ tag.tag_name }}
                        </div>

                    </div>
                </div>
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
                <!-- Для афишы кнопка перехода на календарь битрикса -->
                <div class="news__about-event__wrapper"
                     v-if="currentPost.indirect_data?.bx_event?.ID && currentPost.section_id == 53">
                    <a :href="`https://portal.emk.ru/calendar/?EVENT_ID=${currentPost.indirect_data.bx_event.ID}`"
                       class="primary-button news__about-event__button">
                        Подробнее
                    </a>
                </div>
            </div>
        </div>
        <!-- для новостей орг развития//подвал с фото -->
        <div v-if="(currentPost.section_id == 32) || (sectionId == '32')"
             class="row mb-5">
            <div :to="{ name: 'user', params: { id: user.id } }"
                 v-for="user in (previewElement ? currentPost.users : currentPost.indirect_data?.users)"
                 :key="user.id"
                 class="">
                <RouterLink :to="{ name: 'userPage', params: { id: user.id } }"
                            class="mb-5 news__person-wrap">
                    <figure>
                        <img class="img-fluid img-thumbnail news__person__img"
                             :src=user.photo_file_url
                             data-banner="/upload/resize_cache/main/3e5/gtm4c2ulm9kav603bkxxbqac80k6wo7e/360_206_2/Сальвассер.jpg.png">
                    </figure>
                    <div class="news__person-info">
                        <p class="news__person-fio">{{ user.fio }}</p>
                        <p class="news__person-staff">{{ user.position }}</p>
                    </div>
                </RouterLink>
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import SwiperBlank from "@/components/tools/swiper/SwiperBlank.vue";
import DocIcon from "@/assets/icons/posts/DocIcon.svg?component";
import { defineComponent, type Ref, ref, type PropType, watch } from "vue";
import type { IBaseEntity, IReportage } from "@/interfaces/IEntities";
import Api from "@/utils/Api";
import Reactions from "./Reactions.vue";
import { parseMarkdown } from "@/utils/parseMarkdown";
import type { ITag } from "@/interfaces/entities/ITag";

export interface IPostInner extends IBaseEntity {
    indirect_data?: {
        // Благотв
        organizer?: string,
        phone_number?: string
        // Афиша
        date_from?: string,
        date_to?: string,
        reports?: IReportage[],
        department?: string,
        tags?: ITag[] | number[],
        // орг развитие
        users?: {
            id: number,
            fio: string,
            position: string,
            photo_file_url: string
        }[],
        // афиша
        bx_event?: {
            [key: string]: string
        }
    },
    department?: string,
    reports?: IReportage[],
    // орг развитие
    users?: {
        id: number,
        fio: string,
        position: string,
        photo_file_url: string
    }[],
    // Блоги
    TITLE?: string,
    author?: string

}

export default defineComponent({
    name: 'PostInner',
    components: {
        SwiperBlank,
        DocIcon,
        Reactions
    },
    props: {
        id: {
            type: String || undefined,
        },
        sectionId: {
            type: String
        },
        type: {
            type: String,
            default: 'default'
        },
        previewElement: {
            type: (Object as PropType<IPostInner>) || null
        },
        previewImages: {
            type: Array<string>
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
                if (props.id && typeof props.id == 'string')
                    Api.get(`article/find_by_ID/${props.id}`)
                        .then((res) => {
                            currentPost.value = res;
                            if (!currentPost.value) return;
                            changeToPostStandart(currentPost as Ref<IPostInner>);
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
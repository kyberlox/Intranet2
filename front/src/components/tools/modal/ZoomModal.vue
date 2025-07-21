<template>
    <div class="modal__overlay modal__overlay--zoom"
         @click="close()">
        <div class="modal__overlay__close-button">
            <CloseIcon />
        </div>
        <div class="modal__wrapper modal__wrapper--zoom">
            <div class="modal__body modal__body--zoom">
                <FullWidthSlider v-if="image"
                                 :images="Array.isArray(image) ? image : [image]"
                                 :activeIndex="activeIndex"
                                 :type="'postInner'" />
                <div v-if="video"
                     class="modal__video">
                    <iframe class="modal__video__frame"
                            :src="String(repairVideoUrl(video))"
                            title="video"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen>
                    </iframe>
                </div>
                <div class="modal__text"
                     v-if="textOnly && currentUser">
                    <div class="modal__text__content">
                        <div class="row mb-3">
                            <div class="col">
                                <img :src="currentUser.photo_file_url"
                                     class="img-fluid img-thumbnail modal__text__content__user-photo rounded-circle mx-auto d-block">
                                <div class="text-center mt20">
                                    <strong>{{ currentUser.last_name + " " + currentUser.name + " " +
                                        currentUser.second_name }}</strong><br>
                                    <span class="fw-light">{{ currentUser.indirect_data.work_position }}</span><br>
                                    <span v-for="item in currentUser.indirect_data.uf_usr_1696592324977">
                                        {{ item }}
                                    </span>
                                </div>
                            </div>
                        </div>
                        <div class="row mb-3 justify-content-center">
                            <div class="col-sm-10 col-print-12">
                                <h2 class="page__title text-center">#{{ textContent.number }} {{ textContent.name }}
                                </h2>
                                <div class="mb-3"
                                     id="detail-text"
                                     style="text-align: justify">
                                    {{ textContent.content }}
                                </div>
                                <div>
                                    <button class="btn btn-primary"
                                            id="save-pdf">Сохранить PDF</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { repairVideoUrl } from "@/utils/embedVideoUtil";
import { type PropType } from "vue";
import FullWidthSlider from "@/components/tools/swiper/FullWidthSlider.vue";
import CloseIcon from '@/assets/icons/layout/CloseIcon.svg?component'
export default {
    props: {
        image: {
            type: [Array, String] as PropType<string[] | string>,
        },
        video: {
            type: String,
        },
        activeIndex: {
            type: Number || String,
        },
        textOnly: {
            type: Boolean,
            default: false
        },
        textContent: {
            type: Object
        },
        currentUser: {
            type: Object
        }
    },
    components: {
        FullWidthSlider,
        CloseIcon
    },
    setup(props, { emit }) {
        console.log(props.currentUser.value);

        return {
            close: () => emit("close"),
            repairVideoUrl,
        };
    },
};
</script>
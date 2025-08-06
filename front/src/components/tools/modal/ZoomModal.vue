<template>
    <div class="modal__overlay modal__overlay--zoom"
         @click="close()">
        <div class="modal__overlay__close-button">
            <CloseIcon />
        </div>
        <div class="modal__wrapper modal__wrapper--zoom">
            <div class="modal__body modal__body--zoom">
                <FullWidthSlider v-if="image"
                                 :images="image"
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
                     v-if="textOnly">
                    <div v-if="currentUser"
                         class="modal__text__content">
                        <div class="row mb-3">
                            <div class="col">
                                <img :src="currentUser.photo_file_url"
                                     class="img-fluid img-thumbnail modal__text__content__user-photo rounded-circle mx-auto d-block">
                                <div class="text-center mt20">
                                    <strong>{{ currentUser.last_name + " " + currentUser.name + " " +
                                        currentUser.second_name }}</strong><br>
                                    <span class="fw-light">{{ currentUser.indirect_data.work_position }}</span><br>
                                    <span v-for="(item, index) in currentUser.indirect_data.uf_usr_1696592324977"
                                          :key="'depart' + index">
                                        {{ item }}
                                    </span>
                                </div>
                            </div>
                        </div>
                        <div class="row mb-3 justify-content-center">
                            <div class="col-sm-10 col-print-12">
                                <h2 class="page__title text-center">#{{ textContent?.number }} {{ textContent?.name }}
                                </h2>
                                <div v-if="textContent?.content"
                                     class="mb-3"
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
                    <div class="modal__text__content modal__text__content--points-modal"
                         v-else-if="modalForUserPoints">
                        <div class="row mb-3">
                            <div class="col">
                                <PointsInfoTable />
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
import { defineComponent, type PropType } from "vue";
import FullWidthSlider from "@/components/tools/swiper/FullWidthSlider.vue";
import CloseIcon from '@/assets/icons/layout/CloseIcon.svg?component';
import PointsInfoTable from "@/views/user/userPointsComponents/PointsInfoTable.vue";

interface ImageObject {
    file_url?: string;
}

type ImageItem = string | ImageObject;
type ImageArray = ImageItem[];

export default defineComponent({
    props: {
        image: {
            type: Array as PropType<ImageArray>,
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
        },
        modalForUserPoints: {
            type: Boolean
        }
    },
    components: {
        FullWidthSlider,
        CloseIcon,
        PointsInfoTable
    },
    setup(props, { emit }) {
        return {
            close: () => emit("close"),
            repairVideoUrl,
        };
    },
});
</script>
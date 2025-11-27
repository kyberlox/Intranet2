<template>
<div class="news-inner__page__wrapper mt20">
    <div class="row row-gap-50">
        <div class="col-12 col-lg-6 mb-2 pos-rel">
            <SwiperBlank :images="[{ file_url: String(slugImage()) }]"
                         :type="'postInner'" />
        </div>
        <div class="col-12 col-lg-6">
            <div class="news__detail__content">
                <div class="news__detail__top">
                    <div class="row mb-2">
                        <div class="col-12">
                            <h2 class="news__detail__title">
                                {{ title }}
                            </h2>
                        </div>
                    </div>
                </div>
                <div class="news__detail__discr">
                    {{ text }}
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import SwiperBlank from "@/components/tools/swiper/SwiperBlank.vue";
import { defineComponent } from "vue";
import { chooseImgPlug } from "@/utils/chooseImgPlug";


export default defineComponent({
    name: 'PostSlug',
    components: {
        SwiperBlank
    },
    props: {
        title: {
            type: String
        },
        text: {
            type: String
        }
    },
    setup() {
        return {
            slugImage: chooseImgPlug
        }
    }
})
</script>
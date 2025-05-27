<template>
    <div v-if="currentCource"
         class="currentCource__page mt20">
        <div class="page__title">Электронные курсы</div>

        <div class="cource__section mt20 row">
            <div class="col-12 col-lg-6">
                <div class="cource__main__pict partners__detail__main__pict detail__main__pict">
                    <div class="cource__main__pict__item detail__main__pict__item partners__detail__main__img">
                        <img class="cource__main__pict__item__img news__detail__main__img"
                             :src="currentCource.img"
                             alt="" />
                    </div>
                </div>
            </div>
            <div class="col-12 col-lg-6">
                <div class="cource__detail__inner__content news__detail__content">
                    <div class="row mb-2">
                        <div class="col-12">
                            <h2 class="cource__detail__title news__detail__title mb-2">{{ currentCource.name }}</h2>
                        </div>
                    </div>
                </div>
                <div class="cource__detail__top news__detail__top">
                    <div class="cource__detail__discr news__detail__discr">
                        <h3>Содержание курса</h3>
                        <ul>
                            <li v-for="(item, index) in currentCource.structure"
                                :key="index">{{ item }}</li>
                        </ul>
                    </div>
                    <div class="cource__detail__discr news__detail__discr">
                        <div class="cource__additional-info">
                            <div class="cource__additional-info__item"
                                 v-for="(info, index) in currentCource.additionalInfo"
                                 :key="index">
                                <h3>{{ info.title }}</h3>
                                <p>{{ info.text }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { useRoute } from "vue-router";
import { allCources } from "@/assets/staticJsons/trainingCenterData";
import { defineComponent } from "vue";
export default defineComponent({
    setup() {
        const route = useRoute();
        return {
            currentCource: allCources.find((item) => item.id == Number(route.params.id)),
        };
    },
});
</script>

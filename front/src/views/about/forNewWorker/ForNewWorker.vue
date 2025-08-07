<template>
    <div class="page__title mt20">Памятка новому сотруднику</div>
    <div class="memo__section row">
        <div class="col-12 col-lg-12 col-xl-9 col-xxl-9">
            <div class="memo__items">
                <div class="memo__item__group"
                     id="memo__items__">
                    <div class="memo__item mb-5"
                         v-for="(item, index) in pageContent"
                         :key="index"
                         :id="`memo__item${item.id}`">
                        <div class="row">
                            <div class="col-12 col-md-6 col-lg-6 col-xl-8">
                                <div class="memo__item__main__img__wrapper">
                                    <div v-if="item.preview_file_url"
                                         class="memo__item__main__img"
                                         v-lazy-load="item.preview_file_url"
                                         alt="изображение с памятки">
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-md-6 col-lg-6 col-xl-4">
                                <div class="memo__item__content">
                                    <div class="news__detail__discr"
                                         v-html="item.content_text"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="d-none d-lg-block col-xl-3 col-xxl-3">
            <div class="m_menu_w"></div>
            <div class="memo__menu__wrap d-none d-xl-flex">
                <ul class="memo__menu-dots sticky__menu">
                    <li v-for="item in pageContent"
                        :key="'mark' + item.id"
                        class="memo__menu-dot">
                        <div @click="navigate(item.id)"
                             class="memo__menu-dot__item">{{ item.name }}</div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { sectionTips } from "@/assets/static/sectionTips";
import Api from "@/utils/Api";
import { defineComponent, onMounted, ref } from "vue";
import type { IForNewWorker } from '@/interfaces/IEntities'

export default defineComponent({
    name: "ForNewWorker",
    components: {
        // DocIcon,
    },
    setup() {
        const pageContent = ref<IForNewWorker[]>();
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Новому сотруднику']}`)
                .then((res: IForNewWorker[]) => {
                    pageContent.value = res;
                })
        })
        const navigate = (id: number) => {
            const element = document.getElementById(`memo__item${String(id)}`);
            if (!element) return;
            window.scrollTo({
                top: element.offsetTop - 100,
                behavior: "smooth",
            });
        };
        return {
            pageContent,
            navigate,
        };
    },
});
</script>
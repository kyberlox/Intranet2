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
                                <div class="memo__item__main__img">
                                    <img class="news__detail__main__img"
                                         src="/public/imgs/forNewWorker1.jpg"
                                         alt="" />
                                </div>
                            </div>
                            <div class="col-12 col-md-6 col-lg-6 col-xl-4">
                                <div class="memo__item__content news__detail__discr">
                                    <div v-html="item.textHtml"></div>
                                    <div v-if="item.pdf"
                                         class="link__pdf">
                                        <a :href="file.link"
                                           v-for="(file, index) in item.pdf"
                                           :key="index"
                                           class="document-link">
                                            <strong>
                                                Cкачать
                                                <br />
                                                "{{ file.name }}"
                                            </strong>
                                            <DocIcon />
                                        </a>
                                    </div>
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
                             class="memo__menu-dot__item">{{ item.title }}</div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import DocIcon from "@/assets/icons/posts/DocIcon.svg?component";
import { pageContent } from "@/assets/staticJsons/forNewWorkerMemo";
import { defineComponent } from "vue";
export default defineComponent({
    name: "ForNewWorker",
    components: {
        DocIcon,
    },
    setup() {
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

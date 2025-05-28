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
                                    <img v-if="item.indirect_data.PROPERTY_476[0].includes('http')"
                                         class="news__detail__main__img"
                                         src="/public/imgs/forNewWorker1.jpg"
                                         alt="" />
                                    <img v-else
                                         class="news__detail__main__img"
                                         src="https://placehold.co/360x206"
                                         alt="" />
                                </div>
                            </div>
                            <div class="col-12 col-md-6 col-lg-6 col-xl-4">
                                <div class="memo__item__content">
                                    <div class="news__detail__discr"
                                         v-html="item.indirect_data.PROPERTY_477[0].TEXT"></div>
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
                             class="memo__menu-dot__item">{{ item.name }}</div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import DocIcon from "@/assets/icons/posts/DocIcon.svg?component";
import { sectionTips } from "@/assets/staticJsons/sectionTips";
import Api from "@/utils/Api";
import { defineComponent, onMounted, ref, type PropType } from "vue";

interface IforNewWorkerObject {
    "id": number,
    "active": boolean,
    "content_text": string,
    // "date_publiction": null,
    "indirect_data": {
        "ID": string,
        "IBLOCK_ID": string,
        "NAME": string,
        "PROPERTY_479": [
            string
        ],
        "PROPERTY_475": [
            string
        ],
        "PROPERTY_476": [
            string
        ],
        "PROPERTY_477": [
            {
                "TYPE": string,
                "TEXT": string
            }
        ],
        "PROPERTY_478": [
            string
        ],
        "PROPERTY_480": [
            string
        ],
        "section_id": number,
        "TITLE": string
    },
    "name": string,
    [key: string]: any,
}

export default defineComponent({
    name: "ForNewWorker",
    components: {
        DocIcon,
    },
    setup() {
        const pageContent = ref<IforNewWorkerObject[]>();
        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['Новому сотруднику']}`)
                .then((res: IforNewWorkerObject[]) => {
                    pageContent.value = res.sort((a, b) => {
                        return Number(a.indirect_data.PROPERTY_475[0]) - Number(b.indirect_data.PROPERTY_475[0])
                    })
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
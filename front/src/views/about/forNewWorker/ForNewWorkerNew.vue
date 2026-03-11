<template>
<div class="page__title mt20">Памятка новому сотруднику</div>
<div class="memo__section row">
    <div>
        <button @click="showLocations = !showLocations"
                class="btn dropdown-toggle tagDateNavBar__dropdown-toggle">
            {{ activeLocation ? activeLocation : 'Я работаю в' }}
        </button>
        <CustomFilter v-if="showLocations"
                      :params="locations"
                      :modifiers="['nosort']"
                      @pickFilter="(filter: string) => { showLocations = false; activeLocation = filter; console.log(filter) }" />
    </div>
    <div class="col-12 col-lg-12 col-xl-9 col-xxl-9">
        <div class="memo__items">
            <div class="memo__item__group"
                 id="memo__items__">
                <div class="memo__item"
                     v-for="(item, index) in filterContent(pageContent)"
                     :key="index"
                     :id="`memo__item${item.id}`">
                    <ForNewWorkerCard :item="item" />
                </div>
                <div class="memo__item">
                    <ForNewWorkerCard v-if="endingSlide(pageContent)"
                                      :item="(endingSlide(pageContent) as IForNewWorker)" />
                </div>
            </div>
        </div>
    </div>
    <div class="d-none d-lg-block col-xl-3 col-xxl-3">
        <ul class="memo__menu-dots sticky__menu">
            <li v-for="item in filterContent(pageContent)"
                :key="'mark' + item.id"
                class="memo__menu-dot">
                <div @click="navigate(item.id)"
                     class="memo__menu-dot__item">
                    {{ item.name }}
                </div>
            </li>
        </ul>
    </div>

</div>
</template>

<script lang="ts">
import { sectionTips } from "@/assets/static/sectionTips";
import Api from "@/utils/Api";
import { defineComponent, onMounted, ref } from "vue";
import type { IForNewWorker } from '@/interfaces/IEntities'
import CustomFilter from "@/components/tools/common/CustomFilter.vue";
import ForNewWorkerCard from "./ForNewWorkerCard.vue";

export default defineComponent({
    name: "ForNewWorker",
    components: {
        CustomFilter,
        ForNewWorkerCard
    },
    setup() {
        const pageContent = ref<IForNewWorker[]>([]);
        const activeLocation = ref('');
        const showLocations = ref(false);
        const locations = ref<string[]>([]);

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['НовомуСотруднику']}`)
                .then((res: IForNewWorker[]) => {
                    res.forEach(e => {
                        if (e.indirect_data && 'module' in e.indirect_data && e.indirect_data.module && !locations.value.includes(e.indirect_data.module) && e.indirect_data.module !== 'Заключение') {
                            locations.value.push(e.indirect_data.module)
                        }
                    })
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

        const filterContent = (pageContent: IForNewWorker[]) => {
            return pageContent?.filter(e => e.indirect_data?.module !== 'Заключение' && (!activeLocation.value ? !e.indirect_data?.module : e.indirect_data?.module == activeLocation.value))
        }

        return {
            pageContent,
            navigate,
            filterContent,
            activeLocation,
            showLocations,
            locations,
            endingSlide: (pageContent: IForNewWorker[]) => pageContent.find((e: IForNewWorker) => e.indirect_data && e.indirect_data.module == 'Заключение') || undefined
        };
    },
});
</script>
<style scoped>
.memo__item {
    border-bottom: 1px solid #eaeaea;
    padding-bottom: 30px;
    margin-top: 15px;

    &:not(:first-child) {
        margin-top: 30px;
    }
}

.memo__item:last-child {
    border-bottom: none;
}

.memo__item__main__img__wrapper {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.news__detail__discr {
    line-height: 1.6;
    color: #333;
}

.news__detail__discr b {
    display: block;
    margin-bottom: 10px;
    /* color: #2c3e50; */
    font-size: larger;
    /* color: var(--emk-brand-color-dark); */
    /* text-shadow: var(--emk-brand-color-dark); */
    /* text-shadow: 1px 1px 2px var(--emk-brand-color-dark); */
}

@media (max-width: 767.98px) {
    .memo__item__main__img__wrapper {
        margin-bottom: 15px;
    }
}

@media (min-width: 768px) {
    .memo__item .row {
        align-items: flex-start;
    }

    /* Стили для сайд-навигации */
    .memo__menu__wrap {
        position: sticky;
        top: 100px;
        background: #f9f9f9;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e0e0e0;
    }

    .memo__menu-dots {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .memo__menu-dot {
        border-radius: 8px;
        transition: background-color 0.2s;
    }

    .memo__menu-dot:hover {
        /* background-color: #f4af5a16; */
    }

    .memo__menu-dot__item {
        display: block;
        /* padding: 10px 20px; */
        font-size: 16px;
        color: #333;
        text-decoration: none;
        cursor: pointer;
        font-weight: 500;
        border-left: 3px solid transparent;
        transition: all 0.2s;
    }

    .memo__menu-dot__item:hover {
        color: var(--emk-brand-color);
        border-left-color: var(--emk-brand-color);
        /* background-color: #f4af5a17; */
    }

    /* Адаптивность */
    @media (max-width: 1199.98px) {
        .memo__menu__wrap {
            padding: 20px;
        }

    }
}
</style>
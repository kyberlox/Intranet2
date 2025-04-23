<template>
    <div class="sidebar mt20">
        <div class="tasks__block">
            <Calendar />
        </div>

        <div class="task__block"
             v-for="(workLink, index) in workLinks"
             :key="index">
            <a :href="workLink.href"
               target="_blank">
                <div class="task__block__title">
                    <div class="task_section__item__icon">
                        <Component :is="workLink.icon"
                                   class="support__block__icon support__block__icon--with-outer" />
                    </div>
                    <div class="task__block__portal__link">
                        <h3 class="task__block__portal__link__title">
                            <div href="http://motiw.imp.int/user/"
                                 target="_blank">{{ workLink.title }}</div>
                        </h3>
                        <div class="task__block__portal__link__link"
                             :href="workLink.href"
                             target="_blank">{{ workLink.description }}</div>
                    </div>
                </div>
                <div class="home__view__item__link"
                     target="_blank">{{ workLink.linkTitle }} <span></span></div>
            </a>
        </div>


        <div class="support__blocks">
            <a v-for="(link, index) in supportLinks"
               :href="link.href"
               target="_blank"
               class="support__block"
               :key="index">
                <Component :is="link.icon"
                           class="support__block__icon" />
                <div class="support__block__link__item">
                    <div class="support__block__phone">{{ link.title }}</div>
                    <div class="support__block__link">{{ link.description }}</div>
                </div>
            </a>
        </div>

        <div id="pageArrow"
             style=""
             class="default"><i class="fa fa-arrow-down"
               aria-hidden="true"></i></div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { workLinks } from "@/assets/staticJsons/layoutSidebar";
import { supportLinks } from "@/assets/staticJsons/layoutSidebar";
import Calendar from "./Calendar.vue";

export default defineComponent({
    components: {
        Calendar
    },
    setup() {
        return {
            workLinks,
            supportLinks,
        };
    },
});
</script>
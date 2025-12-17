<template>
<div class="sidebar mt20">
    <div class="task__block">
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
                        {{ workLink.title }}
                    </h3>
                    <h4 class="task__block__portal__link__link"
                        :href="workLink.href"
                        target="_blank">
                        {{ workLink.description }}
                    </h4>
                </div>
            </div>
            <div class="homeview__item__link"
                 target="_blank">
                {{ workLink.linkTitle }}
            </div>
        </a>
    </div>


    <div class="support__blocks">
        <a v-for="(link, index) in supportLinks.filter((e) => e.href == 'bugReport')"
           :key="'bug' + index"
           class="support__block support__block--bug-report"
           @click="callBugReportModal(true)">
            <Component :is="link.icon"
                       class="support__block__icon" />
            <div class="support__block__link__item">
                <div class="support__block__phone">{{ link.title }}</div>
                <div class="support__block__link">{{ link.description }}</div>
            </div>
        </a>
        <a v-for="(link, index) in supportLinks.filter((e) => needAdminLink ? e : e.href !== 'admin' && e.href !== 'bugReport')"
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
</div>
<RightSidebarBugModalVue v-if="bugModalIsVisible"
                         @closeModal="callBugReportModal(false)" />
</template>
<script lang="ts">
import { defineComponent, computed, ref } from "vue";
import { workLinks, supportLinks } from "@/assets/static/navLinks";
import Calendar from "./RightSidebarCalendar.vue";
import { useUserData } from "@/stores/userData";
import RightSidebarBugModalVue from "./RightSidebarBugModal.vue";

export default defineComponent({
    components: {
        Calendar,
        RightSidebarBugModalVue
    },
    setup() {
        const bugModalIsVisible = ref(false);

        const callBugReportModal = (val: boolean) => {
            bugModalIsVisible.value = val;
        }
        return {
            workLinks,
            supportLinks,
            bugModalIsVisible,
            needAdminLink: computed(() => useUserData().getNeedAdminLink),
            callBugReportModal
        };
    },
});
</script>
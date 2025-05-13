<template>
    <div class="refer-page mt20">
        <div class="refer-page__wrapper">
            <div class="refer-page__img"
                 :style="{ 'background': `url(https://portal.emk.ru/intranet/personal/vacancies/referPage.jpg) no-repeat` }">
            </div>
        </div>

        <div class="jobWrapper">
            <div class="jobs-header">
                <h2>Открытые вакансии</h2>
            </div>

            <ul v-if="jobList !== undefined && jobList.length > 0"
                class="job-list">
                <li v-for="job in jobList"
                    :key="job.id">
                    <a :href=job.href
                       target="_blank"
                       class="job-link">
                        {{ job.name }} </a>
                </li>
            </ul>

            <ul v-else>
                <li class="job-link job-link--nohover">
                    В настоящее время открытых вакансий нет
                </li>
            </ul>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';

interface IJobList {
    id: number,
    href: string,
    name: string
}

export default defineComponent({
    setup() {
        const jobList = ref<IJobList[]>();

        return {
            jobList
        }
    }
})
</script>
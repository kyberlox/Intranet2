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
                    <a :href="getProperty(job, 'PROPERTY_5094')"
                       target="_blank"
                       class="job-link">
                        {{ job.name }}
                    </a>
                </li>
            </ul>

            <ul v-else-if="noVac">
                <li class="job-link job-link--nohover">
                    В настоящее время открытых вакансий нет
                </li>
            </ul>

            <ul v-else>
                <li v-for="i in 16"
                    :key="'jobSkelet' + i"
                    class="job-link job-link--nohover skeleton-job-link">
                </li>
            </ul>
        </div>
    </div>
</template>
<script lang="ts">
import { sectionTips } from '@/assets/staticJsons/sectionTips';
import Api from '@/utils/Api';
import { defineComponent, onMounted, ref } from 'vue';
import { getProperty } from '@/utils/getPropertyFirstPos';
import { type IOpenVacancy } from '@/interfaces/IEntities';

export default defineComponent({
    setup() {
        const jobList = ref<IOpenVacancy[]>();
        const noVac = ref(false);

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips["ОткрытыеВакансии"]}`)
                .then((data) => {
                    if (data.length) {
                        jobList.value = data;
                    }
                    else noVac.value = true;
                })
        })

        return {
            jobList,
            getProperty,
            noVac
        }
    }
})
</script>
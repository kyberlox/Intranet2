<template>
    <div class="literature__training__page mt20">
        <div class="page__title">Учебные пособия и литература ЭМК</div>
        <div class="trainings-table__navigation-header">
            <!-- фильтр по авторам -->
            <TagDateNavBar @pickFilter="(e) => pickFilter(e, 'автор')"
                           :modifiers="'noTag'"
                           :buttonText="'Автор'"
                           :params="authors" />
            <!-- фильтр по разделам -->
            <TagDateNavBar @pickFilter="(e) => pickFilter(e, 'раздел')"
                           :buttonText="'Раздел'"
                           :modifiers="'noTag'"
                           :params="sections" />
        </div>
        <TrainingTable :page="'literature'"
                       :tableElements="renderedLiterature" />
    </div>
</template>

<script lang="ts">
import Api from "@/utils/Api";
import TrainingTable from "../components/TrainingTable.vue";
import { defineComponent, onMounted, ref } from "vue";
import { sectionTips } from "@/assets/static/sectionTips";
import TagDateNavBar from "@/components/tools/common/TagDateNavBar.vue";

export default defineComponent({
    components: {
        TrainingTable,
        TagDateNavBar
    },
    setup() {
        const literature = ref();
        const renderedLiterature = ref();
        const authors = ref([]);
        const sections = ref([]);

        const setFilterData = (data) => {
            data.map((e) => {
                if (!authors.value.length || !authors.value.includes(e.indirect_data.author)) {
                    authors.value.push(e.indirect_data.author)
                }
                if (!sections.value.length || !sections.value.includes(e.indirect_data.subsection)) {
                    sections.value.push(e.indirect_data.subsection)
                }
            })
        }

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['УчЛитература']}`)
                .then((e) => {
                    setFilterData(e);
                    literature.value = e;
                    renderedLiterature.value = e;
                })
        })

        const pickFilter = (param, type) => {
            renderedLiterature.value = literature.value;
            if (type == 'автор') {
                renderedLiterature.value = renderedLiterature.value.filter((e) => { return e.indirect_data.author == param });
            }
            else if (type == 'раздел') {
                renderedLiterature.value = renderedLiterature.value.filter((e) => { return e.indirect_data.subsection == param });
            }
        }

        return {
            literature,
            authors,
            sections,
            pickFilter,
            renderedLiterature
        };
    },
});
</script>

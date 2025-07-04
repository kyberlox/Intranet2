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
import { defineComponent, onMounted, ref, type Ref } from "vue";
import { sectionTips } from "@/assets/static/sectionTips";
import TagDateNavBar from "@/components/tools/common/TagDateNavBar.vue";
import type { ItableItem } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        TrainingTable,
        TagDateNavBar
    },
    setup() {
        const literature = ref();
        const renderedLiterature = ref();

        const authors: Ref<string[]> = ref([]);
        const sections: Ref<string[]> = ref([]);

        const setFilterData = (data: ItableItem[]) => {
            data.map((e) => {
                if (!e.indirect_data) return;

                if (!authors.value.length || (e.indirect_data.author && !authors.value.includes(e.indirect_data.author))) {
                    authors.value.push(String(e.indirect_data.author))
                }
                if (!sections.value.length || (e.indirect_data.subsection && !sections.value.includes(e.indirect_data.subsection))) {
                    sections.value.push(String(e.indirect_data.subsection))
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

        const pickFilter = (param: string, type: string) => {
            renderedLiterature.value = literature.value;
            if (type == 'автор') {
                renderedLiterature.value = renderedLiterature.value.filter((e: ItableItem) => { if (e.indirect_data) return e.indirect_data.author == param });
                console.log(renderedLiterature.value);

            }
            else if (type == 'раздел') {
                renderedLiterature.value = renderedLiterature.value.filter((e: ItableItem) => { if (e.indirect_data) return e.indirect_data.subsection == param });
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

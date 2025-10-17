<template>
<div class="literature__training__page mt20">
    <div class="page__title">Учебные пособия и литература ЭМК</div>
    <div class="conducted-training-table__navigation-header">
        <div v-for="(name, index) in ['Автор', 'Раздел']"
             :key="index + 'filter'"
             class="dropdown-wrapper tagDateNavBar__dropdown-wrapper tagDateNavBar__dropdown-wrapper--long">
            <button @click="showThis ? showThis = '' : showThis = name"
                    class="btn btn-light dropdown-toggle tagDateNavBar__dropdown-toggle">
                {{ name }}
            </button>
            <transition name="fade">
                <TagDateNavBar v-if="showThis == name"
                               :modifiers="'noTag'"
                               :buttonText="name"
                               :params="name == 'Автор' ? authors : sections"
                               @pickFilter="(e) => pickFilter(e, name)" />
            </transition>
        </div>
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
import TagDateNavBar from "@/components/tools/common/DateFilter.vue";
import type { ItableItem } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        TrainingTable,
        TagDateNavBar
    },
    setup() {
        const literature = ref();
        const renderedLiterature = ref();
        const showparams = ref(false);
        const authors: Ref<string[]> = ref([]);
        const sections: Ref<string[]> = ref([]);
        const showThis = ref<string>();

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
            if (type == 'Автор') {
                renderedLiterature.value = renderedLiterature.value.filter((e: ItableItem) => { if (e.indirect_data) return e.indirect_data.author == param });
            }
            else if (type == 'Раздел') {
                renderedLiterature.value = renderedLiterature.value.filter((e: ItableItem) => { if (e.indirect_data) return e.indirect_data.subsection == param });
            }
            showThis.value = '';
        }

        return {
            literature,
            authors,
            sections,
            showparams,
            renderedLiterature,
            showThis,
            pickFilter,
        };
    },
});
</script>

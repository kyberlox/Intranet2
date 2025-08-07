<template>
    <div v-if="docs"
         class="experience__page mt20">
        <div class="page__title">Референсы и опыт поставок</div>

        <div class="experience__table">
            <div class="experience__table__row"
                 v-for="(doc, index) in docs"
                 :key="index + 'doc'">
                <a class="experience__table__row"
                   :href="doc.file_url"
                   target="_blank">
                    <div class="experience__table__row__leftside">
                        <div class="experience__table__row__leftside__title conducted-training__list__item__title__one">
                            {{ doc.original_name }}
                        </div>
                        <div
                             class="experience__table__row__leftside__subtitle conducted-training__list__item__title__two">
                            {{ placeName }}
                        </div>
                    </div>
                    <div class="experience__table__row__download-link lib__list__item__file__link">
                        Скачать файл {{ doc.original_name }}
                    </div>
                </a>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch, type Ref } from 'vue';
import { useExperienceData } from "@/composables/useExperienceData";
import { useReferencesAndExpDataStore } from "@/stores/referencesAndExpData";
import type { IDocument } from "@/interfaces/IEntities";

export default defineComponent({
    name: 'experienceType',
    props: {
        factoryId: {
            type: String,
            required: true
        },
        sectorId: {
            type: String,
            required: true
        }
    },
    setup(props) {
        const { loadExperienceData } = useExperienceData();

        const docs: Ref<IDocument[]> = ref([]);
        const placeName = ref('');

        const initializeData = () => {
            const data = loadExperienceData();

            watch(data, (newValue) => {
                if (Object.keys(newValue).length && props.factoryId && props.sectorId) {
                    docs.value = useReferencesAndExpDataStore().getCurrentDocs(props.factoryId, props.sectorId);
                    placeName.value = useReferencesAndExpDataStore().getCurrentFactory(props.factoryId).factoryName;
                };
            }, { immediate: true })
        }
        onMounted(() => {
            initializeData();
        });

        return {
            docs,
            placeName
        };

    }
})

</script>

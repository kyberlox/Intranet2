import { sectionTips } from "@/assets/static/sectionTips";
import { type Ref, ref } from "vue";
import Api from "./Api";
import type { IExperience, IFormattedData } from "@/interfaces/IEntities";
import { useReferencesAndExpDataStore } from "@/stores/ReferencesAndExpData";
import { factoryLogoTips, sectorLogoTips } from "@/assets/static/factoryLogoTips";
export const useExperienceData = () => {
    const formatExperienceItem = (item: IExperience, formattedData: Ref<IFormattedData>) => {
        if (!item.indirect_data) return;

        const industryId = Number(item.indirect_data?.industryId);
        const industryTitle = item.indirect_data?.industry;
        const enterprise = item.indirect_data?.enterprise;
        const enterpriseId = item.indirect_data?.enterpriseId;
        const docs = item.documentation.length > 0 ? item.documentation : item.images;

        if (!industryId || !industryTitle || !enterprise || !enterpriseId) return;

        if (!formattedData.value[enterpriseId]) {
            formattedData.value[enterpriseId] = {
                sectors: [],
                factoryName: enterprise ?? String(enterpriseId),
                factoryId: enterpriseId
            };
        }

        const existingSector = formattedData.value[enterpriseId].sectors
            .find(sector => sector.sectorTitle === industryTitle);

        if (!existingSector) {
            formattedData.value[enterpriseId].sectors.push({
                sectorTitle: industryTitle,
                sectorId: industryId,
                sectorDocs: docs
            });
        } else {
            existingSector.sectorDocs.push(...docs);
        }
    };


    const loadExperienceData = () => {
        const existingData = useReferencesAndExpDataStore().getAllFactories;

        if (Object.keys(existingData).length > 0) {
            return existingData;
        }

        const formattedData: Ref<IFormattedData> = ref({});

        Api.get(`article/find_by/${sectionTips['референсы']}`)
            .then((data) => data.forEach(item => formatExperienceItem(item, formattedData)));

        useReferencesAndExpDataStore().setFactories(formattedData.value);

        return formattedData.value;
    }


    const generateSlides = (data: IFormattedData) => {
        console.log(data);

        const getLogo = (factoryId: string) => {
            return factoryLogoTips[factoryId]
        }

        return Object.keys(data).map(factoryId => ({
            factoryId: Number(factoryId),
            slides: [],
            preview_file_url: getLogo(factoryId),
            name: data[factoryId].factoryName
        }));
    };

    return {
        loadExperienceData,
        generateSlides
    }
}

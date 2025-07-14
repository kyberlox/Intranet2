import Api from "./Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";

export const prefetchSection = (dataType: 'factoryGuid') => {
    const factoryGuidData = useFactoryGuidDataStore();
    switch (dataType) {
        case 'factoryGuid':
            Api.get(`article/find_by/${sectionTips['гидПредприятия']}`)
                .then((data) => {
                    factoryGuidData.setAllFactories(data)
                })
            break;

        default:
            break;
    }
}
import Api from "./Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";
import { getBlogAuthorsToStore } from "./getBlogAuthorsToStore";
import { useblogDataStore } from "@/stores/blogData";
import { useViewsDataStore } from "@/stores/viewsData";
export const prefetchSection = (dataType: 'factoryGuid' | 'blogs' | 'calendar') => {
    const factoryGuidData = useFactoryGuidDataStore();
    switch (dataType) {
        case ('factoryGuid'):
            if (!factoryGuidData.getAllFactories.length)
                Api.get(`article/find_by/${sectionTips['гидПредприятия']}`)
                    .then((data) => {
                        factoryGuidData.setAllFactories(data)
                    })
            break;
        case 'blogs':
            if (!useblogDataStore().getAllAuthors.length)
                getBlogAuthorsToStore();
            break;
        case 'calendar':
            if (!useViewsDataStore().getData('calendarData').length) {
                const currentYear = new Date().getFullYear();
                Api.get(`b24/calendar/${currentYear}-01-01}/${currentYear}-12-31`)
                    .then((data) => {
                        useViewsDataStore().setData(data.result, 'calendarData');
                    });
            }
        default:
            break;
    }
}
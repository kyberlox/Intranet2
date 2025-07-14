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
                fetch(`https://portal.emk.ru/rest/1/f5ij1aoyuw5f39nb/calendar.event.get.json?type=company_calendar&ownerId=0&from=${currentYear}-01-01&to=${currentYear}-12-31`)
                    .then((resp) => resp.json())
                    .then((data) => {
                        useViewsDataStore().setData(data.result, 'calendarData');
                    });
            }
        default:
            break;
    }
}
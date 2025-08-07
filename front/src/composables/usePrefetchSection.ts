import Api from "../utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";
import { getBlogAuthorsToStore } from "./useBlogAuthors";
import { useblogDataStore } from "@/stores/blogData";
import { useViewsDataStore } from "@/stores/viewsData";
import { useUserData } from "@/stores/userData";
export const prefetchSection = (dataType: 'factoryGuid' | 'blogs' | 'calendar' | 'user') => {
    if (!useUserData().isLogin) return;
    const factoryGuidData = useFactoryGuidDataStore();
    switch (dataType) {
        case 'user':
            if (Object.keys(useUserData().getUser).length) return
            Api.get(`users/find_by/${useUserData().getMyId}`)
                .then((res) => {
                    useUserData().setUserInfo(res);
                })
            break;
        case 'factoryGuid':
            if (!factoryGuidData.getAllFactories.length)
                Api.get(`article/find_by/${sectionTips['гидПредприятиям']}`)
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
                Api.get(`b24/calendar/${currentYear}-01-01/${currentYear}-12-31`)
                    .then((data) => {
                        useViewsDataStore().setData(data.result, 'calendarData');
                    });
            }
        default:
            break;
    }
}
import Api from "../utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";
import { getBlogAuthorsToStore } from "./useBlogAuthors";
import { useblogDataStore } from "@/stores/blogData";
import { useViewsDataStore } from "@/stores/viewsData";
import { useUserData } from "@/stores/userData";
import { useUserScore } from "@/stores/userScoreData";

export const prefetchSection = (dataType: 'factoryGuid' | 'blogs' | 'calendar' | 'user' | 'score') => {
    if (!useUserData().isLogin) return;
    const factoryGuidData = useFactoryGuidDataStore();
    switch (dataType) {
        case 'user':
            Api.get(`users/find_by/${useUserData().getMyId}`)
                .then((res) => {
                    useUserData().setUserInfo(res);
                    localStorage.setItem('user', res);
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
            break;
        case 'score':
            const scoreRoutes = [{
                route: '/peer/sum',
                functionName: useUserScore().setCurrentScore
            },
            {
                route: '/peer/actions',
                functionName: useUserScore().setActions
            },
            {
                route: '/peer/statistics',
                functionName: useUserScore().setStatistics
            }]
            scoreRoutes.map((e) => {
                Api.get(e.route)
                    .then((data) => {
                        e.functionName(data);
                    });
            })
            break;
    }
}
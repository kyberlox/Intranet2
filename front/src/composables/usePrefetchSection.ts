import Api from "../utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { useFactoryGuidDataStore } from "@/stores/factoryGuid";
import { getBlogAuthorsToStore } from "./useBlogAuthors";
import { useblogDataStore } from "@/stores/blogData";
import { useViewsDataStore } from "@/stores/viewsData";
import { useUserData } from "@/stores/userData";
import { useUserScore } from "@/stores/userScoreData";
import { usePointsData } from "@/stores/pointsData";
import { featureFlags } from "@/assets/static/featureFlags";

export const prefetchSection = async (dataType: 'factoryGuid' | 'blogs' | 'calendar' | 'user' | 'score') => {
    if (!useUserData().isLogin) return;
    const factoryGuidData = useFactoryGuidDataStore();
    const blogStore = useblogDataStore();
    switch (dataType) {
        case 'user':
            try {
                const res = await Api.get(`users/find_by/${useUserData().getMyId}`)
                useUserData().setUserInfo(res);
                const userRes = await Api.get('roots/get_root_token_by_uuid')
                if (userRes && typeof userRes == 'object' && (Object.keys(userRes).length !== 0)) {
                    useUserData().setUserRoots(userRes);
                }
            }
            catch (error) {
                console.error(error)
            }
            break;
        case 'factoryGuid':
            if (!factoryGuidData.getAllFactories.length)
                try {
                    const data = await Api.get(`article/find_by/${sectionTips['гидПредприятиям']}`)
                    factoryGuidData.setAllFactories(data)
                } catch (error) {
                    console.error(error)
                }
            break;
        case 'blogs':
            if (blogStore.getAllAuthors.length) return;
                getBlogAuthorsToStore();
            break;
        case 'calendar':
            const currentYear = new Date().getFullYear();
            try {
                const data = await Api.get(`b24/calendar/${currentYear}-01-01/${currentYear}-12-31`)
                useViewsDataStore().setData(data?.result, 'calendarData');
            } catch (error) {
                console.error(error)
            }
            break;
        case 'score':
            if (featureFlags.pointsSystem) {
                const scoreRoutes = [
                    {
                        route: '/peer/actions',
                        functionName: useUserScore().setActions
                    },
                    {
                        route: '/peer/user_history',
                        functionName: useUserScore().setStatistics
                    },
                    {
                        route: '/peer/get_all_activities',
                        functionName: usePointsData().setAllActivities
                    }
                ]

                scoreRoutes.map(async (e) => {
                    await Api.get(e.route)
                        .then((data) => {
                            e.functionName(data);
                        });
                })
            }
            break;
    }
}
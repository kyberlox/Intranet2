import { defineStore } from "pinia";
import type { INews, IAfishaItem, ICareSlide, ICorpLife, IOurPeople, IVideoInterview, IVideoReports, IFactoryGuidSlides, IBaseEntity } from "@/interfaces/IEntities";
import type { MainPageCards } from "@/interfaces/IMainPage";
import type { ICalendar } from "@/interfaces/entities/ICalendar";

interface DataState {
    homeData: MainPageCards,
    ourPeopleData: IOurPeople[],
    actualNewsData: INews[],
    corpEventsData: INews[],
    corpLifeData: ICorpLife[],
    afishaData: IAfishaItem[],
    careData: ICareSlide[],
    videoInterviewsData: IVideoInterview[],
    videoReportsData: IVideoReports[],
    corpNewsData: INews[],
    officialEventsData: IBaseEntity[],
    partnerBonusData: IBaseEntity[],
    calendarData: ICalendar[],
    factoryGuidData: IFactoryGuidSlides[],
    // yearResultsData: any[];
    // blogsData: any[];
    // gazettesData: any[],
}

type DataStateKey = keyof DataState;

export const useViewsDataStore = defineStore('viewsData', {
    state: (): DataState => ({
        homeData: [],
        ourPeopleData: [],
        videoInterviewsData: [],
        actualNewsData: [],
        corpNewsData: [],
        videoReportsData: [],
        officialEventsData: [],
        corpEventsData: [],
        corpLifeData: [],
        afishaData: [],
        partnerBonusData: [],
        careData: [],
        calendarData: [],
        factoryGuidData: [],
        // yearResultsData: [],
        // blogsData: [],
        // gazettesData: any[],
    }),

    actions: {
        setData<T extends DataStateKey>(fetchedData: DataState[T], dataType: T): void {
            if (this[dataType]) {
                (this[dataType] as DataState[T]) = fetchedData;
            }
            else console.error(`uknown ${dataType}`);
        }
    },

    getters: {
        getData: (state) => (dataType: DataStateKey) => {
            return state[dataType]
        }
    }
});
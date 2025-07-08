import { defineStore } from "pinia";
import type { IActualNews, IAfishaItem, ICareSlide, ICorpLife, ICorpEventsItem, IOurPeople, IVideoInterview, IVideoReports, ICorpNews, IOfficialEvents, IPartnerBonus } from "@/interfaces/IEntities";
import type { MainPageCards } from "@/interfaces/IMainPage";
import type { ICalendar } from "@/interfaces/ICalendar";

interface DataState {
    homeData: MainPageCards,
    ourPeopleData: IOurPeople[],
    actualNewsData: IActualNews[],
    corpEventsData: ICorpEventsItem[],
    corpLifeData: ICorpLife[],
    afishaData: IAfishaItem[],
    careData: ICareSlide[],
    videoInterviewsData: IVideoInterview[],
    videoReportsData: IVideoReports[],
    corpNewsData: ICorpNews[],
    officialEventsData: IOfficialEvents[],
    partnerBonusData: IPartnerBonus[],
    calendarData: ICalendar[]
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
        calendarData: []
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
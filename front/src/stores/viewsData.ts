import { defineStore } from "pinia";
import type { IActualNews, IAfishaItem, ICareSlide, ICorpLife, ICorpEventsItem } from "@/interfaces/IEntities";
import type { MainPageCards } from "@/interfaces/IMainPage";

interface DataState {
    homeData: MainPageCards,
    ourPeopleData: any[],
    // yearResultsData: any[];
    // blogsData: any[];
    videoInterviewsData: any[],
    actualNewsData: IActualNews[],
    corpNewsData: any[],
    videoReportsData: any[],
    // gazettesData: any[],
    officialEventsData: any[],
    corpEventsData: ICorpEventsItem[],
    corpLifeData: ICorpLife[],
    afishaData: IAfishaItem[],
    partnerBonusData: any[],
    careData: ICareSlide[],
}

// Определяем тип для ключей состояния
type DataStateKey = keyof DataState;

export const useViewsDataStore = defineStore('viewsData', {
    state: (): DataState => ({
        homeData: [],
        ourPeopleData: [],
        // yearResultsData: [],
        // blogsData: [],
        videoInterviewsData: [],
        actualNewsData: [],
        corpNewsData: [],
        videoReportsData: [],
        // gazettesData: any[],
        officialEventsData: [],
        corpEventsData: [],
        corpLifeData: [],
        afishaData: [],
        partnerBonusData: [],
        careData: [],
    }),

    actions: {
        setData(fetchedData, dataType: DataStateKey) {
            if (this[dataType]) {
                this[dataType] = fetchedData;
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
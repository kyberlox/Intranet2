import { defineStore } from "pinia";

// Определяем тип для состояния хранилища
interface DataState {
    homeData: any[],
    ourPeopleData: any[],
    // yearResultsData: any[];
    // blogsData: any[];
    videoInterviewsData: any[],
    actualNewsData: any[],
    corpNewsData: any[],
    videoReportsData: any[],
    // gazettesData: any[],
    officialEventsData: any[],
    corpEventsData: any[],
    corpLifeData: any[],
    afishaData: any[],
    partnerBonusData: any[],
    careData: any[],
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
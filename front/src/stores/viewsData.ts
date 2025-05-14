import { defineStore } from "pinia";

export const useViewsDataStore = defineStore('viewsData', {
    state: () => ({
        homeData: [],
        ourPeopleData: [],
    }),

    actions: {
        setHomeData(fetchedData) {
            this.homeData = fetchedData;
        },
        setOurPeopleData(fetchedData) {
            this.ourPeopleData = fetchedData;
        }
    },

    getters: {
        getHomeData: (state) => state.homeData,
        getOurPeopleData: (state) => state.ourPeopleData
    }
});
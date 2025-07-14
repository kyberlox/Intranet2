import { defineStore } from "pinia";
import type { IFactoryGuidSlides, IFactoryDataTours, IFactoryDataReports } from "@/interfaces/IEntities";

export const useFactoryGuidDataStore = defineStore('FactoryGuidData', {
    state: () => ({
        allFactories: [] as IFactoryGuidSlides[],
        factoryReports: [] as IFactoryDataReports[],
        factoryTours: [] as IFactoryDataTours[],
    }),

    actions: {
        setAllFactories(data: IFactoryGuidSlides[]) {
            this.allFactories = data;
        },
    },

    getters: {
        getAllFactories: (state) => state.allFactories,
        getCurrentFactory: (state) => (x: number) => state.allFactories.find((e) => e.id == x),
        getFactoryReports: (state) => (x: number) => state.allFactories.find((e) => e.id == x)?.indirect_data?.reports,
        getFactoryTours: (state) => (x: number) => state.allFactories.find((e) => e.id == x)?.indirect_data?.tours,
    }
});
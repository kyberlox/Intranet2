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
        getCurrentFactory: (state) => (factoryId: number) => state.allFactories.find((e) => e.id == factoryId),
        getFactoryReports: (state) => (factoryId: number) => state.allFactories.find((e) => e.id == factoryId)?.indirect_data?.reports,
        getFactoryTours: (state) => (factoryId: number) => state.allFactories.find((e) => e.id == factoryId)?.indirect_data?.tours,
        getFactoryTour: (state) => (factoryId: number, tourId: string) => state.allFactories.find((e) => e.id == factoryId)?.indirect_data?.tours?.find((e) => e.id == Number(tourId))
    }
});
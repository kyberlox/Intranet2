import { defineStore } from "pinia";
import type { IExperience, IFormattedData } from "@/interfaces/IEntities";

export const useReferencesAndExpDataStore = defineStore('referencesAndExpData', {
    state: () => ({
        allFactories: {} as IFormattedData,
    }),

    actions: {
        setFactories(factories: IFormattedData) {
            this.allFactories = factories;
        }
    },

    getters: {
        getAllFactories: (state) => state.allFactories,
        getCurrentFactory: (state) => (id: string) => state.allFactories[id],
        getCurrentDocs: (state) => (id: string, sector: string) => state.allFactories[id].sectors.find(e => e.sectorId == sector)?.sectorDocs,
    }
});
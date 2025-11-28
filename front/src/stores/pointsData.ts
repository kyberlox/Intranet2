import { defineStore } from "pinia";

import { type IActivitiesList } from "@/interfaces/IEntities";


export const usePointsData = defineStore('pointsData', {
    state: () => ({
        allActivities: [] as IActivitiesList[]
    }),

    actions: {
        setAllActivities(actives: IActivitiesList[]) {
            this.allActivities = actives
        },
    },

    getters: {
        getActivities: (state) => state.allActivities,
        getActivitiesToConfirm: (state) => state.allActivities.filter((e) => e.need_valid == true),
    }
});

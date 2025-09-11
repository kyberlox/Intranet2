import { defineStore } from "pinia";
import { type IActivityToSend } from "@/interfaces/IEntities";

export const useUserScore = defineStore('userScoreData', {
    state: () => ({
        currentScore: 0,
        availableActions: {} as IActivityToSend,
        statistics: [],
    }),

    actions: {
        setCurrentScore(score: number) {
            this.currentScore = score
        },
        setActions(actions: IActivityToSend) {
            this.availableActions = actions;
        },
        setStatistics(statData: any) {
            this.statistics = statData;
        }
    },

    getters: {
        getCurrentScore: (state) => state.currentScore,
        getActions: (state) => state.availableActions,
        getStatistics: (state) => state.statistics
    }
});
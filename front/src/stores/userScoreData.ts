import { defineStore } from "pinia";

export const useUserScore = defineStore('userScoreData', {
    state: () => ({
        currentScore: 0,
        availableActions: [''],
        statistics: [],
    }),

    actions: {
        setCurrentScore(score: number) {
            this.currentScore = score
        },
        setActions(actions: string[]) {
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
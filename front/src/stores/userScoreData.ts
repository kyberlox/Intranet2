import { defineStore } from "pinia";
import type {  IActivityToSend, IActivityStatistics } from "@/interfaces/IEntities";

export const useUserScore = defineStore('userScoreData', {
    state: () => ({
        currentScore: 0,
        availableActions: {} as IActivityToSend,
        statistics: [] as IActivityStatistics[]
    }),

    actions: {
        setCurrentScore(score: number) {
            this.currentScore = score
        },
        setActions(actions: IActivityToSend) {
            this.availableActions = actions;
        },
        setStatistics(statData: IActivityStatistics[]) {
            this.statistics = statData;
            let score = 0;
            if(statData.length){
            statData.forEach((e)=>{
                 score += e.cost
            });
        }
            this.setCurrentScore(score);
        }
    },

    getters: {
        getCurrentScore: (state) => state.currentScore,
        getActions: (state) => state.availableActions,
        getStatistics: (state) => state.statistics
    }
});
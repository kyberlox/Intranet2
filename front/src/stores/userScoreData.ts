import { defineStore } from "pinia";
import type {  IActivityToSend, IActivityStatistics } from "@/interfaces/IEntities";

const MERCH_STORE_SENDER = "магазин мерча";

const normalizeHistoryText = (value: unknown) => String(value ?? "").trim().toLocaleLowerCase("ru-RU");

const isMerchPurchase = (activity: IActivityStatistics) => {
    const senderName = normalizeHistoryText(activity.fio_from);
    const activityName = normalizeHistoryText(activity.activity_name);

    return senderName === MERCH_STORE_SENDER
        || activityName.includes("покуп")
        || activityName.includes("снятие баллов")
        || Number(activity.cost ?? 0) < 0;
};

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
            const statistics = Array.isArray(statData) ? statData : [];
            this.statistics = statistics;
            const score = statistics.reduce((sum, item) => sum + Number(item.cost ?? 0), 0);
            this.setCurrentScore(score);
        }
    },

    getters: {
        getCurrentScore: (state) => state.currentScore,
        getActions: (state) => state.availableActions,
        getStatistics: (state) => state.statistics,

        getPurchaseHistory: (state) => state.statistics.filter(isMerchPurchase),
        getAdditionHistory: (state) => state.statistics.filter((activity) => !isMerchPurchase(activity))
    }
});

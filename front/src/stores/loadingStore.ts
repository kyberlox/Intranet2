import { defineStore } from "pinia";

export const useLoadingStore = defineStore('loadingStore', {
    state: () => ({
        loading: false,
    }),

    actions: {
        setLoadingStatus(status: boolean) {
            this.loading = status
        }
    },

    getters: {
        getLoadingStatus: (state) => state.loading,
    }
});
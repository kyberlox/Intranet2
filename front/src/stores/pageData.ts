import { defineStore } from "pinia";

export const usePageDataStore = defineStore('pageData', {
  state: () => ({
    currentRoute: '',
  }),

  actions: {
    setCurrentRoute(route: string) {
      this.currentRoute = route
    }
  },

  getters: {
    getCurrentRoute: (state) => state.currentRoute,
  }
});
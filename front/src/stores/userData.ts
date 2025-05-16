import { defineStore } from "pinia";

export const useUserData = defineStore('userData', {
    state: () => ({
        myId: '2366',
    }),

    actions: {
        setMyId(id: string) {
            this.myId = id;
        },
    },

    getters: {
        getMyId: (state) => state.myId
    }
});
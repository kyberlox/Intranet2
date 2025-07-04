import { defineStore } from "pinia";

export const useUserData = defineStore('userData', {
    state: () => ({
        myId: 2366,
        authKey: '',
        isLogin: false
    }),

    actions: {
        setMyId(id: number) {
            this.myId = id;
        },
        setLogin(login: boolean) {
            this.isLogin = login;
        },
        setAuthKey(key: string) {
            this.authKey = key;
        },
        initKeyFromStorage() {
            const storedAuthKey = localStorage.getItem('authKey');
            if (!storedAuthKey) return
            this.authKey = String(storedAuthKey);
            this.isLogin = true;
        },
        logOut() {
            this.authKey = '';
            this.isLogin = false;
            localStorage.removeItem('authKey');
        }
    },

    getters: {
        getMyId: (state) => state.myId,
        getIsLogin: (state) => state.isLogin,
        getAuthKey: (state) => state.authKey
    }
});
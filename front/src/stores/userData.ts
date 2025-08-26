import { defineStore } from "pinia";
import type { IUser } from "@/interfaces/IEntities";

export const useUserData = defineStore('userData', {
    state: () => ({
        myId: 0,
        authKey: '',
        user: {} as IUser,
        isLogin: false
    }),

    actions: {
        setMyId(id: number) {
            this.myId = id;
            localStorage.setItem('id', String(id));
        },
        setLogin(login: boolean) {
            this.isLogin = login;
        },
        setAuthKey(key: string) {
            this.authKey = key;
            localStorage.setItem('key', key);
        },
        initKeyFromStorage() {
            const storedAuthKey = localStorage.getItem('authKey');
            const storedId = localStorage.getItem('id');
            if (!storedAuthKey) return
            this.authKey = String(storedAuthKey);
            this.myId = Number(storedId);
            this.isLogin = true;
        },
        setUserInfo(userData: IUser) {
            this.user = userData;
        },
        logOut() {
            this.authKey = '';
            this.isLogin = false;
            this.user = {} as IUser;
            this.myId = 0;
            localStorage.removeItem('authKey');
            localStorage.removeItem('id');
        }
    },

    getters: {
        getMyId: (state) => state.myId,
        getIsLogin: (state) => state.isLogin,
        getAuthKey: (state) => state.authKey,
        getUser: (state) => state.user,
        getPhoto: (state) => state.user.photo_file_url,
        getFio: (state) => state.user.last_name + ' ' + state.user.name + ' ' + state.user.second_name
    }
});
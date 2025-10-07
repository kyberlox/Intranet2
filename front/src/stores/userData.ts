import { defineStore } from "pinia";
import type { IUser } from "@/interfaces/IEntities";
import type{ IRoots } from "@/interfaces/IEntities";

export const useUserData = defineStore('userData', {
    state: () => ({
        myId: 0,
        authKey: '',
        user: {} as IUser,
        roots: {PeerAdmin: false, EditorAdmin: false, VisionAdmin: false} as IRoots,
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
        setUserRoots(data: IRoots){
            this.roots.EditorAdmin = data.EditorAdmin
            this.roots.VisionAdmin = data.VisionAdmin
            this.roots.PeerAdmin = data.PeerAdmin
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
        getUserRoots: (state)=> state.roots,
        getNeedAdminLink: (state) => state.roots.EditorAdmin || state.roots.PeerAdmin || state.roots.VisionAdmin,
        getUser: (state) => state.user,
        getPhoto: (state) => state.user.photo_file_url,
        getFio: (state) => state.user.last_name + ' ' + state.user.name + ' ' + state.user.second_name,
        getSignature: (state) => (`С уважением,
${state.user.last_name + ' ' + state.user.name + ' ' + state.user.second_name}
--
АО «НПО «ЭМК»
Тел.: ${state.user.uf_phone_inner}
Моб.: ${state.user.personal_mobile}
Эл. почта: ${state.user.email} `)
    }
});
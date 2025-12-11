import { defineStore } from "pinia";
import type { IUser } from "@/interfaces/IEntities";
import type{ IRoots } from "@/interfaces/IEntities";

export const useUserData = defineStore('userData', {
    state: () => ({
        myId: 0,
        authKey: '',
        user: {} as IUser,
        roots: {PeerAdmin: false, EditorAdmin: false, VisionAdmin: false, EditorModer: []} as IRoots,
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
            const storedAuthKey = document?.cookie?.split(';')?.find((e)=> e.includes('session_id'))?.replace(' session_id=', '');
            const storedId = document?.cookie?.split(';')?.find((e)=> e.includes('user_id'))?.replace(' user_id=', '');
            if (!storedAuthKey) return
            this.authKey = String(storedAuthKey);
            this.myId = Number(storedId);
            this.isLogin = true;
        },
        setUserInfo(userData: IUser) {
            this.user = userData;
        },
        setUserRoots(data: IRoots){
            this.roots = data
        },
        logOut() {
            this.authKey = '';
            this.isLogin = false;
            this.user = {} as IUser;
            this.myId = 0;
            document.cookie.split(';').forEach(function(c) {
            document.cookie = c.trim().split('=')[0] + '=;' + 'expires=Thu, 01 Jan 1970 00:00:00 UTC;';
        });
        }
    },

    getters: {
        getMyId: (state) => state.myId,
        getIsLogin: (state) => state.isLogin,
        getAuthKey: (state) => state.authKey,
        getUserRoots: (state)=> state.roots,
        getNeedAdminLink: (state) => state.roots.EditorAdmin || state.roots.PeerAdmin || state.roots.VisionAdmin || (state.roots.EditorModer && state.roots.EditorModer.length),
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

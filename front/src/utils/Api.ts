import axios from 'axios';
import { useUserData } from "@/stores/userData";
import { computed } from "vue";
import { type IAuth } from '@/interfaces/IPostFetch';

const VITE_API_URL = import.meta.env.VITE_API_URL;
const authKey = computed(() => useUserData().getAuthKey);

const api = axios.create({
    baseURL: VITE_API_URL,
    withCredentials: true,
    headers: { 'Content-Type': 'application/json' }
});

// добавляю токен
api.interceptors.request.use(config => {
    config.headers.Authorization = authKey.value;
    return config;
});

export default class Api {
    static async get(url: string) {
        return (await api.get(url)).data;
    }

    static async post(url: string, data: IAuth) {
        return (await api.post(url, data)).data;
    }
}

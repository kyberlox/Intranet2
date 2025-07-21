import axios, { AxiosError } from 'axios';
import { useUserData } from "@/stores/userData";
import { computed } from "vue";
import type { IPostIdea, IAuth } from '@/interfaces/IPostFetch';

const VITE_API_URL = import.meta.env.VITE_API_URL;
const authKey = computed(() => useUserData().getAuthKey);

const api = axios.create({
    baseURL: VITE_API_URL,
    withCredentials: true,
    // headers: { 'Content-Type': 'application/json' }
});

// добавляю токен
api.interceptors.request.use(config => {
    config.headers.Authorization = authKey.value;
    return config;
});

export default class Api {
    static async get(url: string) {
        try {
            return (await api.get(url)).data;
        } catch (error) {
            if (error instanceof AxiosError && error.response?.status == 401) {
                useUserData().logOut();
                throw new Error('Сессия истекла. Необходимо войти в систему заново.');
            }
            throw error;
        }
    }

    static async post(url: string, data: IAuth | IPostIdea) {
        return (await api.post(url, data)).data;
    }

    static async put(url: string) {
        return (await api.put(url))
    }
}

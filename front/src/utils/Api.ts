import axios, { AxiosError, type AxiosRequestConfig } from 'axios'
import { useUserData } from '@/stores/userData'
import { computed } from 'vue'
import type { IPostIdea, IAuth, IValidatePoints, IUsersLoad, IPostEventToExcell } from '@/interfaces/IPostFetch'
import type { IPointsForm, INewActivityData, IPurchaseMerchData } from '@/interfaces/IPutFetchData'
import type { IPostCardMsg, INeuroChat } from '@/interfaces/IEntities'
import type { IPostInner } from '@/components/tools/common/PostInner.vue'

const VITE_API_URL = import.meta.env.VITE_API_URL
const api = axios.create({
    baseURL: VITE_API_URL,
    withCredentials: true,
})

const vendorApi = axios.create({
    withCredentials: true,
})

// добавляю токен
const authCookie = computed(()=> useUserData().getAuthKey);;
api.interceptors.request.use((config) => {
    config.headers.session_id = authCookie.value || ''
    return config
})

export default class Api {
    static async get(url: string) {
        try {
            return (await api.get(url)).data
        } catch (error) {
            if (error instanceof AxiosError && error.response?.status == 401) {
                useUserData().logOut()
                throw new Error('Сессия истекла. Необходимо войти в систему заново.')
            }
            throw error
        }
    }

    static async postVendor(url: string, data: INeuroChat[] | null | FormData) {
        return (await vendorApi.post(url, data)).data
    }

    static async post(
        url: string,
        data?:
            | IAuth
            | IPostIdea
            | IPostInner
            | FormData
            | IPostCardMsg
            | IValidatePoints
            | INewActivityData
            | IUsersLoad
            | Array<IPostEventToExcell>
            | null,
            config?: AxiosRequestConfig
    ) {
    const req = api.post(url, data, config);
    return config ? (await req) : (await req).data
    }

    static async put(
        url: string,
        data?: number[] | IPointsForm | INewActivityData | IPurchaseMerchData,
    ) {
        return (await api.put(url, data)).data
    }

    static async delete(url: string, data?: number[]) {
        return await api.delete(url, { data })
    }
}

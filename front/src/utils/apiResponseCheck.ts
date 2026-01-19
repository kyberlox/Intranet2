import type { AxiosError, AxiosResponse } from "axios";

interface IToastMethods {
    showError: (type: string) => void,
    showSuccess: (type: string) => void
}

export const handleApiResponse = (data: AxiosResponse, toast: IToastMethods, errorName: string, successName: string) => {
    if (!data || ((typeof data == 'object' && 'data' in data && Boolean(data.data) == false) || typeof data == 'object' && 'error' in data)) {
        toast.showError(errorName);        
    }
    else
        toast.showSuccess(successName);
}

export const handleApiError = (error: AxiosError, toast: IToastMethods) => {    
    if (error.response?.status === 401) {
        toast.showError('authorizatonError');
    }
    else{        
        toast.showError('serverError');
    }
    }

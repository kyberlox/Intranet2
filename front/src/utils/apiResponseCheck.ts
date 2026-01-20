import type { AxiosError, AxiosResponse } from "axios";

interface IToastMethods {
    showError: (type: string) => void,
    showSuccess: (type: string) => void,
    showCustomToast: (type: string, text: string) => void
}

export const handleApiResponse = (data: AxiosResponse | {'status': string}, toast: IToastMethods, errorName: string, successName: string) => {
    if ((!data || ((typeof data == 'object' && 'data' in data && Boolean(data.data) == false)) )) {
        toast.showError(errorName);        
    }
    else if (data?.status && typeof data.status == 'string' ){
        toast.showCustomToast(data.status, errorName)
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

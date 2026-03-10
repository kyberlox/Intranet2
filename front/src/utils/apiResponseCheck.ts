import type { AxiosError, AxiosResponse } from "axios";

interface IToastMethods {
    showError: (type: string) => void,
    showSuccess: (type: string) => void,
    showCustomToast: (type: string, text: string) => void
}

export const handleApiResponse = (data: AxiosResponse | {'status': string} | true, toast: IToastMethods, errorName: string, successName: string) => {
    if(data == true){
       return toast.showSuccess(successName);
    }
    if ((!data || ((typeof data == 'object' && 'data' in data && Boolean(data.data) == false)))) {
       return toast.showError(errorName);        
    }
    else if (((data as {'status': string})?.status == 'warn' || (data as {'status': string})?.status == 'error') 
        && typeof (data as {'status': string}).status == 'string' ){
       return toast.showCustomToast((data as {'status': string}).status, errorName);
    }
    else
       return toast.showSuccess(successName);
}

export const handleApiError = (error: AxiosError | boolean, toast: IToastMethods) => {        
    if(error !== true) {
    if ((error as AxiosError).response?.status === 401) {
       return toast.showError('authorizatonError');
    }
    else{        
      return  toast.showError('serverError');
    }
    }
}

import type { ToastServiceMethods } from "primevue/toastservice";

interface messageGroup { [key: string]: string }

interface messages {
    success: messageGroup
    error: messageGroup
}

const messages: messages = {
    error: {
        trySupportError: 'Что-то пошло не так, попробуйте обновить страницу и повторить или сообщите в поддержку сайта (5182/5185)',
        authorizatonError: 'Необходимо заново авторизоваться, пожалуйста, обновите страницу и попробуйте еще раз',
        serverError: 'Ошибка сервера, пожалуйста, сообщите в поддержку сайта (5182/5185)'
    },
    success: {
        adminDeleteSuccess: 'Элемент успешно удален',
        adminAddElementSuccess: 'Элемент успешно добавлен'
    }
}

export const useToastCompose = (toastInstance: ToastServiceMethods) => {

    const showToast = (type: keyof messages, name: keyof messageGroup) => {
        toastInstance.add({ severity: type, summary: '', detail: messages[type][name], life: 13000 });
    }

    const showSuccess = (name: keyof messageGroup) => {
        showToast('success', name)
    }

    const showError = (name: keyof messageGroup) => {
        showToast('error', name)
    }

    return {
        showToast,
        showSuccess,
        showError,
    };
}
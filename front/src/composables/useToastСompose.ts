import type { ToastServiceMethods } from "primevue/toastservice";

interface messageGroup { [key: string]: string }

interface messages {
    success: messageGroup
    error: messageGroup
    warn: messageGroup
}

const messages: messages = {
    error: {
        trySupportError: 'Что-то пошло не так, попробуйте обновить страницу и повторить или сообщите в поддержку сайта (5182/5185)',
        authorizatonError: 'Необходимо заново авторизоваться, пожалуйста, обновите страницу и попробуйте еще раз',
        serverError: 'Ошибка сервера, пожалуйста, сообщите в поддержку сайта (5182/5185)'
    },
    success: {
        adminDeleteSuccess: 'Элемент успешно удален',
        adminAddElementSuccess: 'Элемент успешно добавлен',
        adminUpdateElementSuccess: 'Элемент успешно обновлен',
        pointsSendSuccess: 'Баллы успешно отправлены',
        ideaSendSuccess: 'Идея успешно отправлена! Спасибо!',
        merchBuySuccess: 'Ваш запрос успешно отправлен! Скоро с вами свяжутся для уточнения',
        EventExcellSuccess: '',
        sendPostCardSuccess: 'Открытка успешна отправлена!'
    },
    warn:{
        merchBuyWarning: 'Покупка станет доступна чуть позже, пока только для ознакомления',
        noUserVCard: 'Сотрудник не найден'
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

    const showWarning = (name: keyof messageGroup) => {
        showToast('warn', name)
    }

    return {
        showToast,
        showSuccess,
        showError,
        showWarning
    };
}

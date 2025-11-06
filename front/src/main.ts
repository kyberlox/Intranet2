import "bootstrap/dist/css/bootstrap.css"
import "bootstrap/dist/js/bootstrap.js"
import '@/assets/styles/_main.scss'
import VueDatePicker from '@vuepic/vue-datepicker';

import '@vuepic/vue-datepicker/dist/main.css'
import PrimeVue from 'primevue/config';
import FileUpload from 'primevue/fileupload';
import ToastService from 'primevue/toastservice';

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { vLazyLoad } from './customDirectives/lazyLoad'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.directive('lazy-load', vLazyLoad)
app.component('VueDatePicker', VueDatePicker);
app.component('FileUpload', FileUpload);

app.use(createPinia())
    .use(router)
    .use(ToastService)
    .use(PrimeVue, {
        locale: {
            upload: 'Загрузить',
            choose: 'Добавить',
            cancel: 'Отмена',
            noFileChosenMessage: 'Файлы не выбраны',
            pending: 'Готов к загрузке',
            browse: 'Добавить',
        }
    })

app.mount('#app')
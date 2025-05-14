import "bootstrap/dist/css/bootstrap.css"
import "bootstrap/dist/js/bootstrap.js"
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import PrimeVue from 'primevue/config';
import ProgressBar from 'primevue/progressbar';

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.component('VueDatePicker', VueDatePicker);
app.component('progressBar', ProgressBar);

app.use(createPinia())
    .use(router)
    .use(PrimeVue)

app.mount('#app')
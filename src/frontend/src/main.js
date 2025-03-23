import '@/core/define' //вспомогательные функции для базовых объектов
import App from '@/App.vue'
import { createApp } from 'vue'

import '@/assets/fontawesome.all.css'
import components from '@/core/defineComponents'

import { api } from '@/api/api'
import { LS } from '@/core/LS'
import { router } from '@/core/router'
import { i18n } from '@/core/i18n'
import { store } from '@/core/store'
// import { notifications } from '@/core/notifications'

const app = createApp(App)
app.config.unwrapInjectedRef = true

// Глобальная регистрация компонентов
Object.entries(components).forEach(([key, value]) => {
    app.component(key, value)
})

// Установка глобальных параметров через provide
app.provide('$t', i18n)
app.provide('$ls', LS)

// Подключение плагинов
app.use(LS).use(i18n).use(router).use(api).use(store)

app.mount('#app')

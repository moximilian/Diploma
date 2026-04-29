import '@/core/define'
import App from '@/App.vue'
import { createApp } from 'vue'
import components from '@/core/defineComponents'

import { api } from '@/api/api'
import { LS } from '@/core/LS'
import { router } from '@/core/router'
import { i18n } from '@/core/i18n'
import { store } from '@/core/store'
import { PROJECT_NAME } from '@/core/settings'

const app = createApp(App)
app.config.unwrapInjectedRef = true
document.title = PROJECT_NAME

// Global component registry
Object.entries(components).forEach(([key, value]) => {
    app.component(key, value)
})

// app.provide('$t', i18n)
app.provide('$ls', LS)

// Plugins connect
app.use(LS).use(i18n).use(router).use(api).use(store)

app.mount('#app')

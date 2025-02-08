import { reactive } from 'vue'
import LocalStorage from '@/core/LocalStorage'

export const LS = new (function () {
    this.ls = null

    this.install = (app, options) => {
        app.config.globalProperties.$ls = this.ls = reactive(
            options?.ls instanceof LocalStorage ? options.ls : new LocalStorage()
        )
    }
})()

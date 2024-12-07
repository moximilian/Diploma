// @ts-check

import { callApi as baseCallApi } from '@/api/api.help'
import { reactive } from 'vue'

// import { Confirmation } from '@/core/notifications'

/**
 * Возвращает функцию вызова api
 * Для улучшения читабельности и уменьшения повторяющегося кода
 *
 * @param { String } path
 * @param { Function } setArgsFn
 * @returns { Function } callApi function
 */
const makeApiFn =
    (path, setArgsFn = args => ({ args })) =>
    (args, cb) =>
        baseCallApi(path, setArgsFn(args), cb)

const customApi = {
    auth: {
        login: makeApiFn('/auth/login'),
        register: makeApiFn('/auth/register'),
        logout: makeApiFn('/auth/logout'),
    },
    items: {
        list: makeApiFn('/items/list'),
    },
    users: {
        one: makeApiFn('/user/get')
    }
}
export const api = new (function () {
    this.api = null

    // eslint-disable-next-line no-unused-vars
    this.install = (app, _) => {
        app.config.globalProperties.$api = this.api = reactive(customApi)
    }
})()

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
        one: makeApiFn('/user/get'),
        update: makeApiFn('/user/update'),
        change_password: makeApiFn('/user/change_password'),
    },
    images: {
        get: makeApiFn('/images/get'),
        set_user: makeApiFn('/images/set_user'),
        delete_user: makeApiFn('/images/delete_user'),
    },
    groups: {
        insert: makeApiFn('/groups/create'),
        one: makeApiFn('/groups/get'),
        list: makeApiFn('/groups/list'),
        update: makeApiFn('/groups/update'),
        delete: makeApiFn('/groups/delete'),
        enter: makeApiFn('/groups/enter'),
        leave: makeApiFn('/groups/leave'),
    },
    participants: {
        list: makeApiFn('/participants/list'),
        delete: makeApiFn('/participants/delete'),
    },
    enter_requests: {
        list: makeApiFn('/groups/requests/list'),
        revoke: makeApiFn('/groups/requests/revoke'),
        accept: makeApiFn('/groups/requests/approve'),
    },
}
export const api = new (function () {
    this.api = null

    // eslint-disable-next-line no-unused-vars
    this.install = (app, _) => {
        app.config.globalProperties.$api = this.api = reactive(customApi)
    }
})()

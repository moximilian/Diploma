// @ts-check

import { callApi as baseCallApi, sendRequest } from '@/api/api.help'
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
    (args) => baseCallApi(path, setArgsFn(args))

const customApi = {
    auth: {
        login: makeApiFn('/auth/login'),
        register: makeApiFn('/auth/register'),
        logout: makeApiFn('/auth/logout'),
        yandexGetData: (token, format, cb) => {
            sendRequest(
                `https://login.yandex.ru/info?format=${format}`,
                'GET',
                {
                    Authorization: token,
                },
                null,
                cb
            )
        },
    },
    items: {
        list: makeApiFn('/items/list'),
    },
    users: {
        one: makeApiFn('/user/get'),
        update: makeApiFn('/user/update'),
        list: makeApiFn('/user/list'),
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

        send_request: makeApiFn('/groups/requests/create'),
    },
    participants: {
        one: makeApiFn('/participants/get'),
        list: makeApiFn('/participants/list'),
        delete: makeApiFn('/participants/delete'),
    },
    enter_requests: {
        list: makeApiFn('/groups/requests/list'),
        revoke: makeApiFn('/groups/requests/revoke'),
        accept: makeApiFn('/groups/requests/approve'),
    },
    events: {
        insert: makeApiFn('/events/create'),
        one: makeApiFn('/events/get'),
        list: makeApiFn('/events/list'),
        update: makeApiFn('/events/update'),
    },
    eventParticipant: {
        list: makeApiFn('/event_participans/list'),
        add_one: makeApiFn('/event_participans/add_one'),
        add_all: makeApiFn('/event_participans/add_all'),
        delete: makeApiFn('/event_participans/delete'),
        update: makeApiFn('/event_participans/update'),
    },
    slotParticipants: {
        list: makeApiFn('/slot_participans/list'),
        update: makeApiFn('/slot_participans/update'),
    },
    slots: {
        insert: makeApiFn('/slots/create'),
        one: makeApiFn('/slots/get'),
        list: makeApiFn('/slots/list'),
        update: makeApiFn('/slots/update'),
        leave: makeApiFn('/slots/leave'),
        enter: makeApiFn('/slots/enter'),
    },
}
export const api = new (function () {
    this.api = null

    // eslint-disable-next-line no-unused-vars
    this.install = (app, _) => {
        app.config.globalProperties.$api = this.api = reactive(customApi)

    }
})()

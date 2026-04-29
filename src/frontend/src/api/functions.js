// @ts-check
import { returnObject, compose, checkString } from '@/core/functions'
import { API_PREFIX, isProductionMode } from '@/core/settings'
import LocalStorage from '@/core/LocalStorage'

/**
 * @typedef {Object} APIParams
 * @property {Object=} headers
 * @property {Object=} body
 * @property {Object=} args
 * @property {String=} method
 * @property {String=} path
 * @property {String=} url
 */

const makeOnError =
    (errors = []) =>
    (...messages) => {
        errors.push(...((messages?.length && messages) || ['Unknown API error.']))
        return errors
    }

const redirect = url => window.location.replace(url || '/auth/login')

const parseHandler = res => {
    const onError = makeOnError(res.errors)
    if (!checkString(res.body)) return { errors: onError('Response body is invalid.') }

    const body = (() => {
        try {
            return JSON.parse(res.body)
        } catch (_) {
            return null
        }
    })()

    body?.status && body?.detail && onError(body.detail)
    body?.error && onError(body.error)
    body?.errors?.length && onError(...body.errors)
    res.body = body

    return res
}

const makeErrorHandler = msg =>
    compose(res => {
        checkString(res.body) || makeOnError(res.errors)(msg)
        return res
    }, parseHandler)

const makeRedirectHandler = (msg, path, cb) => res => (cb?.(), redirect(path), makeOnError(res.errors)(msg), res)

const emptyLS = () => {
    const ls = new LocalStorage()
    ls.setItemEncrypt('current_user', null)
    ls.setItemEncrypt('token', null)
}

const handlersByStatusCode = {
    200: parseHandler,
    201: parseHandler,
    400: makeErrorHandler('[400] Bad Request.'),
    401: makeRedirectHandler('[401] Unauthorized.', '/auth/login', emptyLS),
    403: makeErrorHandler('[403] Forbidden.'),
    404: makeErrorHandler('[404] Not Found.'),
    500: makeErrorHandler('[500] Internal server error.'),
}

/*** Main API methods ***/
/**
 * 
 * @param {APIParams} params 
 * @returns 
 */
const callXhr = ({ url, method, headers, body }) =>
    new Promise(resolve => {
        const Xhr = new XMLHttpRequest()
        const setXhr = (method, object) => Object.entries(object).forEach(args => Xhr[method](...args))
        const onResolve = (statusCode, body, errors) => void resolve({ statusCode, body, errors })
        const onError = (...errors) => onResolve(null, null, errors)

        Xhr.open(method, url)

        setXhr('addEventListener', {
            error: onError,
            load: ({ target: { status, statusText, response } }) => {
                if (status === 0 || statusText === null) return onError('Request timeout.')
                onResolve(status, response, [])
            },
        })

        setXhr('setRequestHeader', {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + new LocalStorage().getItemDecrypt('token'),
            ...headers,
        })

        Xhr.send(body)
    })
/**
 * 
 * @param {Promise<any>} promise 
 * @param {} handlers 
 * @returns 
 */
const handleRequest = (promise, handlers) =>
    promise.then(res => {
        const handler =
            Object.assign(handlersByStatusCode, handlers)[res.statusCode] || (() => res.errors.push('Bad status code.'))
        return Object.assign(res, compose(returnObject, handler)(res))
    })

/**
 * 
 * @param {APIParams} params 
 * @returns {Object}
 */
const makeArguments = ({ path, method, args, headers }) => {
    return {
        url: API_PREFIX + path + (method === 'GET' && args ? '?' + new URLSearchParams(args).toString() : ''),
        method: method === 'GET' ? method : 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...headers,
        },
        credentials: isProductionMode ? false : 'same-origin',
        mode: isProductionMode ? 'cors' : 'same-origin',
        referrerPolicy: 'no-referrer',
        body: method === 'GET' ? null : JSON.stringify(args),
    }
}

/**
 * @param {String} path
 * @param {APIParams} params
 * @param {Object} statusCodeHandlers
 * @returns {Promise<{statusCode: number, body: any, errors: string[], ok: boolean}>}
 */
export const callApi = async (path, params = {}, statusCodeHandlers = {}) => {
    const { method = 'POST', args = {}, headers = {} } = params

    const result = await compose(
        promise => handleRequest(promise, statusCodeHandlers),
        callXhr,
        makeArguments
    )({ path, method, args, headers })
    return {
        ...result,
        ok: result.errors.length === 0,
    }
}

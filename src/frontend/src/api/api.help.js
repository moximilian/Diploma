// @ts-check

// import { notifications } from '@/core/notifications'
import { returnObject, compose, checkString } from '@/core/functions'
import {
    API_PREFIX,
    isProductionMode,
    RESPONSE_SIZE_MB,
    TOTAL_RESPONSE_SIZE_MB,
} from './api.settings'
import LocalStorage from '@/core/LocalStorage'
// import { translate } from './api.help.localization'

/*** Help methods for response ***/

/**
 * @param { Array } errors
 * @returns { Function }
 */
const makeOnError =
    (errors = []) =>
    /**
     * @param { ...String } messages message in error as "throw 'msg'"
     * @return { String[] }
     */
    (...messages) => {
        errors.push(...((messages?.length && messages) || ['Unknown API error.']))
        return errors
    }
/**
 * Redirect function
 * For Development mode redirect on login page
 * @param { String } url
 */
const redirect = url => window.location.replace(url || '/auth/login')
/**
 * @param { Object } res
 * @returns { Object | String | { value: Object, text: String } } parsed body
 * @throws { String }
 */
const parseHandler = res => {
    const onError = makeOnError(res.errors)
    if (!checkString(res.body)) return { errors: onError('Response body is invalid.') }

    const body = (() => {
        try {
            return JSON.parse(res.body)
        } catch (_) {
            _
        }
        try {
            return {
                value: new DOMParser().parseFromString(res.body, 'text/xml'),
                text: res.body,
            }
        } catch (_) {
            _
        }
    })()

    body?.status && body?.detail && onError(body.detail)
    body?.error && onError(body.error)
    body?.errors?.length && onError(...body.errors)
    res.body = body

    return res
}
/**
 * Make function with default error message
 * Function parsing response to get error or error message
 * @param { String } msg Default error message
 * @returns { Function } Throw parsed response error or default message
 */
const makeErrorHandler = msg =>
    compose(res => {
        checkString(res.body) || makeOnError(res.errors)(msg)
        return res
    }, parseHandler)
const makeRedirectHandler = (msg, path) => res => (
    redirect(path), makeOnError(res.errors)(msg), res
)
const handlersByStatusCode = {
    200: parseHandler,
    201: parseHandler,
    202: parseHandler,
    203: makeRedirectHandler('[203] Redirect.', '/'),
    400: makeErrorHandler('[400] Bad Request.'),
    401: makeRedirectHandler('[401] Unauthorized.', '/auth/login'),
    403: makeErrorHandler('[403] Method Not Allowed!.'),
    404: makeErrorHandler('[404] Not Found!.'),
    405: makeErrorHandler('[405] Method Not Allowed!.'),
    408: makeErrorHandler('[408] Request Timeout!.'),
    410: makeErrorHandler('[410] Resource is no available!.'),
    413: makeErrorHandler('[413] Request Entity Too Large!.'),
    429: makeErrorHandler('[429] Too Many Requests!.'),
    500: makeErrorHandler('[500] Internal server error.'),
}

/*** Help methods for request ***/

/** @type {{ maxTotalSize: Number, maxRespSize: Number, size: Number, list: Map, calcSize: Function, getRequestFns: Function, errorMsg: 'Large data set.' }} */
const Buffer = {
    /** States */
    maxTotalSize: TOTAL_RESPONSE_SIZE_MB,
    maxRespSize: RESPONSE_SIZE_MB,
    size: 0,
    list: new Map(),
    /**
     * @param { any } data
     * @param { Number } divideOn default 1024 * 1024
     * @returns { Number } size of data
     */
    calcSize: (data, divideOn = 1024 * 1024) => new Blob([data]).size / divideOn,
    /** @returns {{ add: Function, sum: Function }} */
    getRequestFns: () => {
        let size = 0
        const { calcSize, maxRespSize, maxTotalSize } = Buffer
        return {
            // @ts-ignore
            add: data => (size += calcSize(data) <= maxRespSize) && size + Buffer.size <= maxTotalSize,
            sum: data => (Buffer.size += calcSize(data)),
        }
    },
    errorMsg: 'Large data set.',
}
/**
 * @param { Object } params contains params for request
 * @param { String } params.url
 * @param { String } params.method method of request
 * @param { Object } params.headers headers in request
 * @param { String | FormData } params.body body in request
 * @param { String } params.cache
 * @returns { Promise<{ statusCode: Number, body: Object, errors: String[] }> }
 */
const callXhr = ({ url, method, headers, body, ...params }) =>
    new Promise(resolve => {
        const Xhr = new XMLHttpRequest()
        const setXhr = (method, object) =>
            Object.entries(object).forEach(args => Xhr[method](...args))
        const onResolve = (statusCode, body, errors) => void resolve({ statusCode, body, errors })
        const onError = (...errors) => onResolve(null, null, errors)
        const { add, sum } = Buffer.getRequestFns()

        Xhr.open(
            method,
            url /* url + !(isDevelopmentMode || API_USE_MOCK) ? '' : (/\?/.test(url) ? "&" : "?") + new Date().getTime(), true */
        )

        setXhr('addEventListener', {
            progress: ({ target: { response } }) =>
                checkString(response) && (add(response) || Xhr.abort()),
            error: onError,
            abort: () => onError(Buffer.errorMsg),
            load: ({ target: { status, statusText, response } }) => {
                if (status === 0 || statusText === null) return onError('Request timeout.')

                sum(response)
                onResolve(status, response, [])
            },
        })

        setXhr('setRequestHeader', {
            'Cache-Control': params.cache,
            'Referrer-Policy': 'no-referrer',
            ...headers,
        })
        // Xhr.withCredentials = true

        Buffer.size >= Buffer.maxTotalSize ? onError(Buffer.errorMsg) : Xhr.send(body)
    })
/**
 * @param { Promise<{ statusCode: Number, body: Object, errors: String[] }> } promise
 * @param { Object } handlers
 * @returns { Promise<{ statusCode: Number, body: Object, errors: String[] }> }
 */
const handleRequest = (promise, handlers) =>
    promise.then(res => {
        const handler =
            Object.assign(handlersByStatusCode, handlers)[res.statusCode] ||
            (() => res.errors.push('Bad status code.'))

        return Object.assign(res, compose(returnObject, handler)(res))
    })
/**
 * @param { Promise<{ statusCode: Number, body: Object, errors: String[] }> } promise
 * @returns { Promise<{ statusCode: Number, body: Object, errors: String[] }> }
 */
const handleResult = promise =>
    promise.then(({ statusCode, body, errors }) => {
        const groupName = `API [${statusCode}][${errors.length}]`
        console.log('groupCollapsed', groupName)
        console.log('info', body, errors)
        return { statusCode, body, errors }
    })
/**
 * @param { Object } params contains params for request
 * @param { String } params.path path to api
 * @param { String } params.method method of request
 * @param { Object } params.args headers in request
 * @param { Object } params.headers body in request
 * @returns {{
 *  url           : String,
 *  method        : String,
 *  mode          : String,
 *  cache         : String,
 *  credentials   : String | Boolean,
 *  referrerPolicy: String,
 *  headers       : { 'Content-Type': String },
 *  body          : String | FormData,
 * }}
 */
const makeArguments = ({ path, method, args, headers }) => {
    headers = headers?.['Content-Type']?.includes('form')
        ?
          (delete headers['Content-Type'], headers)
        :
          {
              ...returnObject(headers),
              'Content-Type': 'application/json',
              // @ts-ignore
              Authorization: 'Bearer ' + new LocalStorage().getItemDecrypt('token'),
          }
    const bodyList = Array.isArray(args) ? args : returnObject(args)

    return {
        url:
            API_PREFIX +
            path +
            (method === 'GET' && args ? '?' + new URLSearchParams(args).toString() : ''),
        method: method === 'GET' ? method : 'POST',
        mode: isProductionMode // isDevelopmentMode || API_USE_MOCK)
            ? 'cors'
            : 'same-origin',
        cache: 'no-cache',
        credentials: isProductionMode ? false : 'same-origin',
        referrerPolicy: 'no-referrer',
        headers,
        body: headers?.['Content-Type']
            ? JSON.stringify(bodyList)
            : Object.entries(bodyList).reduce(
                  (form, [key, value]) => (form.append(key, value), form),
                  new FormData()
              ),
    }
}

/**
 * Use in api/index as method for api
 *
 * @param { String } path
 * @param {{ method: String, args: Object, headers: Object }} params
 * @param { Function } cb
 * @returns { Promise<{ $data } | { value, text: String } | undefined> }
 */
export const callApi = async (path, params, cb, statusCodeHandlers) => {
    console.log({ path, params, cb })
    return await compose(
        handleResult,
        promise => handleRequest(promise, returnObject(statusCodeHandlers)),
        callXhr,
        makeArguments
    )({ path, ...params }).then(result =>
        cb(result.body, {
            ...result,
            ok: result.errors.length === 0,
        })
    )
    //  console.log('error', 'API Endpoint miss callback argument')
}

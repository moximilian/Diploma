// @ts-check

/** Application settings -- /public/settings.js */ // @ts-ignore
const settings = window?.settings || {}

/** Modes */
export const isDevelopmentMode = process.env.NODE_ENV === 'development'
export const isProductionMode = process.env.NODE_ENV === 'production'
export const isStandMode = process.env.NODE_ENV === 'stand'

/** Settings */
/** @param { String } key @returns { any } */
const getSetting = key => (isProductionMode && settings[key]) || process.env['VUE_APP_' + key]
/** @param { String } val @param { String } def @returns { String } */
const getStrOr = (val, def = '/') => (typeof val === 'string' && val.trim()) || def
export const PROJECT_NAME = getStrOr(getSetting('PROJECT_NAME'), 'PROJECT NAME')
export const BASE_URL = getStrOr(getSetting('BASE_URL'))
export const API_PATH = getStrOr(getSetting('BASE_API'), '/diploma')
export const TOTAL_RESPONSE_SIZE_MB =
    parseFloat(getSetting('VUE_APP_API_TOTAL_RESPONSE_SIZE_MB')) || 2048
export const RESPONSE_SIZE_MB = parseFloat(getSetting('VUE_APP_API_RESPONSE_SIZE_MB')) || 2
export const NOTI_TIMEOUT_MS = parseFloat(getSetting('NOTI_TIMEOUT_MS')) || 5_000
export const NOTI_ERRORS_TIMEOUT = getSetting('NOTI_ERRORS_TIMEOUT') + '' === 'true'

/** Env files */
export const API_DOMAIN = (!isProductionMode && process.env.VUE_APP_PROXY) || BASE_URL
export const USE_MOCK_ACL = !isProductionMode && process.env.VUE_APP_USE_MOCK_ACL === 'true'
export const API_TIMING_MS = !isProductionMode && 100
export const YANDEX_CLIENT_ID = getSetting('YANDEX_CLIENT_ID')
export const GOOGLE_CLIENT_ID = getSetting('GOOGLE_CLIENT_ID')
/** Other */
export const API_PREFIX =
    API_DOMAIN.endsWith('/') && API_PATH.startsWith('/')
        ? API_DOMAIN + API_PATH.substring(1)
        : API_DOMAIN + API_PATH

export const API_IMG_PREFIX = isProductionMode ? '' : process.env.VUE_APP_API_DOMAIN || ''

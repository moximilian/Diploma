import { reactive } from 'vue'
import CryptoJS from 'crypto-js'

export default class LocalStorage {
    _ls = null
    _secret = /*metaData.userId ||*/ process.env.VUE_APP_CRYPTO_KEY || 'Fghk%^8vmn'
    _theme = false
    _lang = 'en'

    constructor() {
        this._ls = window.localStorage
        let theme = false
        if (theme !== false) theme = Boolean(Number(theme))
        this._theme = theme

        this._lang = ''
        this._token = this.getItemDecrypt('token') || ''

        return reactive(this)
    }

    get theme() {
        return this._theme
    }
    get token() {
        return this._token
    }
    get lang() {
        return this._lang
    }

    set theme(value) {
        this._theme = value
        this.setItemEncrypt('theme', Number(value))
    }

    set token(value) {
        this._token = value
        this.setItemEncrypt('token', value)
    }

    set lang(value) {
        this._lang = value
        this.setItemEncrypt('lang', value)
    }

    setSecret(value) {
        this._secret = value
    }

    removeItem(key) {
        this._ls.removeItem(key)
    }

    subscribe(key, cb) {
        window.addEventListener('storage', event => {
            if (event.key === key) cb?.()
        })
    }
    getItemDecrypt(key) {
        let result = this._ls.getItem(key)
        try {
            result = result
                ? CryptoJS.AES.decrypt(result, this._secret).toString(CryptoJS.enc.Utf8)
                : ''
        } catch (e) {
            result = ''
        }
        return result
    }

    setItemEncrypt(key, value) {
        try {
            value = value ? CryptoJS.AES.encrypt(value, this._secret).toString() : ''
        } catch (e) {
            value = ''
        }
        this._ls.setItem(key, value)
    }
}

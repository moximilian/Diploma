import en from '@/langs/en.json'
import ru from '@/langs/ru.json'
import { createI18n } from 'vue-i18n'

export const i18n = createI18n({
    locale: localStorage.getItem('lang') || 'en',
    fallbackLocale: 'en',
    legacy: false,
    allowComposition: true,
    messages: {
        en,
        ru,
    },
})

const tOriginal = i18n.global.t
const tExist = i18n.global.te
function getTranslateArgs(keys) {
    const [firstKey] = keys

    const key = keys.find(k => tExist(k))
    if (key) return key

    const splittedKeys = firstKey.split('.')
    if (splittedKeys.at(0) === 'models') {
        splittedKeys.splice(1, 1)
        const dotKeys = splittedKeys.join('.')
        const lowerDotKeys = dotKeys.toLocaleLowerCase()
        return tExist(lowerDotKeys) ? lowerDotKeys : dotKeys
    }
    if (splittedKeys.at(0) === 'pagenames') {
        splittedKeys.splice(0, 1)
        return splittedKeys.join('.')
    }

    return firstKey.toLocaleLowerCase()
}

function t(...args) {
    const translateArgs = getTranslateArgs(args)
    const translateCheck = (...params) => (tExist(...params) ? tOriginal(...params) : params[0])

    if (typeof translateArgs === 'number') {
        return translateCheck(translateArgs)
    }

    if (typeof args[1] === 'object') {
        return translateCheck(args[0], args[1])
    }

    if (!tExist(translateArgs)) {
        return args.length > 1
            ? translateCheck(args[1])
            : translateCheck(translateArgs.split('.').pop())
    }

    return translateCheck(translateArgs)
}

i18n.global.t = t

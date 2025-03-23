function defineFunction(target, name, value, enumerable = false) {
    Object.defineProperty(target, name, { value, enumerable })
}

defineFunction(String.prototype, 'ucFirst', function () {
    return this.charAt(0).toUpperCase() + this.slice(1)
})

defineFunction(String.prototype, 'lcFirst', function () {
    return this.charAt(0).toLowerCase() + this.slice(1)
})

defineFunction(String.prototype, 'unCaseString', function () {
    let string = this.trim()
    string = string.replace(/-|_/g, ' ')
    string = string.replace(/[A-Z]/g, match => ` ${match.toLowerCase()}`)
    return string.trim()
})

defineFunction(String.prototype, 'toCamelCase', function () {
    return this.unCaseString().replace(/\s\w/g, match => match[1].toUpperCase())
})
defineFunction(String.prototype, 'toPascalCase', function () {
    return this.toCamelCase().ucFirst()
})
defineFunction(String.prototype, 'toSnakeCase', function () {
    return this.unCaseString().replace(/\s\w/g, match => `_${match[1]}`)
})

// Date

defineFunction(Date, 'init', function (value) {
    if (value instanceof Date) return value

    if (value.split('-')[0].length === 4) {
        const newDate = new this(value)
        if (newDate != 'Invalid Date') return newDate
    }

    const fixTime = time => {
        const times = time.split(':')
        if (times.length < 2) times.push(0)
        return times.map(val => (val < 10 ? `0${val}` : val)).join(':')
    }
    const fixTheOrder = separator => {
        const [date, time] = value.split(' ')
        const [d, m, y] = date.split(separator)
        return new this(`${y}-${m}-${d}` + (time ? ` ${fixTime(time)}` : ''))
    }
    if (!value) return new this()
    if (value.includes('-')) return fixTheOrder('-')
    if (value.includes('.')) return fixTheOrder('.')
})

defineFunction(Date.prototype, 'toShowDate', function (isShown = true) {
    let y = this.getFullYear(),
        m = this.getMonth() + 1,
        d = this.getDate()
    if (d < 10) d = `0${d}`
    if (m < 10) m = `0${m}`
    return isShown ? `${d}-${m}-${y}` : `${y}-${m}-${d}`
})

defineFunction(Date.prototype, 'toShowTime', function (isShownSeconds = false) {
    let h = this.getHours(),
        m = this.getMinutes()
    if (h < 10) h = `0${h}`
    if (m < 10) m = `0${m}`
    let res = `${h}:${m}`
    if (isShownSeconds) {
        let s = this.getSeconds()
        if (s < 10) s = `0${s}`
        res += `:${s}`
    }
    return res
})

defineFunction(Date.prototype, 'toShow', function (isShown = true, isShownSeconds = false) {
    return this.toShowDate(isShown) + ' ' + this.toShowTime(isShownSeconds)
})

defineFunction(Date.prototype, 'isEquals', function (otherDate) {
    if (!(otherDate instanceof Date)) otherDate = Date.init(otherDate)
    return (
        this.getDate() == otherDate.getDate() &&
        this.getMonth() == otherDate.getMonth() &&
        this.getFullYear() == otherDate.getFullYear()
    )
})

// Array

defineFunction(Array.prototype, 'isEquals', function (value) {
    return (
        Array.isArray(this) &&
        Array.isArray(value) &&
        this.length === value.length &&
        this.every((val, index) => val === value[index])
    )
})

// Object

defineFunction(Object, 'combine', function (arrayKeys, arrayValues) {
    const obj = {}
    arrayKeys.forEach((key, index) => {
        obj[key] = arrayValues[index]
    })
    return obj
})

defineFunction(Object, 'isEmpty', function (obj) {
    for (const prop in obj) {
        if (this.hasOwn(obj, prop)) {
            return false
        }
    }

    return true
})
defineFunction(Object, 'isObject', function (obj) {
    return !!obj && typeof obj === 'object'
})

// Array

defineFunction(Array, 'isEmpty', function (arr) {
    return this.isArray(arr) && arr.length === 0
})

defineFunction(Array, 'deepSearch', function (arr, item, key = null) {
    return arr
        .map(function search(element) {
            var result = false
            if (Array.isArray(element)) {
                result = element.map(search).filter(value => !!value)
            } else if (typeof element === 'object' && key && !element?.[key]) return result

            const searchable = (key && element?.[key]) || element
            if (searchable?.includes(item) || searchable === item) {
                result = element
            }
            return result
        })
        .filter(value => !!value)
})

// Function

defineFunction(Function.prototype, 'throttle', function (delayMs = 1000) {
    let fn = this,
        timerId = null
    return function (...args) {
        timerId === null &&
            (fn.apply(this, args), (timerId = setTimeout(() => (timerId = null), delayMs)))
    }
})

defineFunction(Function.prototype, 'debounce', function (delayMs = 1000) {
    let fn = this,
        timerId
    return function (...args) {
        clearTimeout(timerId)
        timerId = setTimeout(() => fn.apply(this, args), delayMs)
    }
})

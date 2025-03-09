exports.returnObject = (object, keys = null, noneValues = 'not set') => {
    if (!object || !(object.toString() === '[object Object]')) {
        return {}
    }
    keys = Array.isArray(keys) ? keys : Object.keys(object)
    noneValues =
        Array.isArray(noneValues) && noneValues.length
            ? noneValues
            : noneValues === 'not set'
            ? [undefined, null, Infinity]
            : [noneValues]

    return keys.reduce(
        (clearObj, key) =>
            !noneValues.includes(object?.[key]) ? { ...clearObj, [key]: object?.[key] } : clearObj,
        {}
    )
}
exports.addGroupEventListeners = (target = document, events = {}, controller = new AbortController()) => {
    Object.entries(events).forEach(([name, fn]) => target.addEventListener(
        name,
        fn,
        { signal: controller.signal }
    ))
    return controller
}

exports.compose =
    (...fns) =>
    x =>
        fns.reduceRight((acc, fn) => fn(acc), x)
exports.checkString = (...strList) =>
    strList.every(str => typeof str === 'string' && !!str.trim().length)

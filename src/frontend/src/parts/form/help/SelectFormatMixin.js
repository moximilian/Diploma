export default {
    inject: {
        localModelName: {
            from: 'modelName',
        },
    },
    methods: {
        getValue(val) {
            if ('object' === typeof val)
                return (
                    val?.text ||
                    val.value ||
                    Object.keys(val)
                        .map(key => val[key])
                        .join(',')
                )
            return val
        },
        getKey(key) {
            return this.checkFunction(
                'keyFormat',
                key,
                'object' === typeof key
                    ? key?.key || key?.id || key.value || key[Object.keys(key)[0]]
                    : key
            )
        },
        showValue(val) {
            return this.checkFunction('showFormat', val, this.translate(this.getValue(val)))
        },
        translate(value) {
            const translateValue = `models.${
                this.localModelName ? this.localModelName + '.' : ''
            }values.${value}`
            const defaultValue = [null, undefined].includes(value) ? '' : value
            return this.$t(translateValue, this.$t(`${value}`, defaultValue))
        },
        checkFunction(name, param, otherwise) {
            return 'function' === typeof this[name]
                ? this[name](param, this.options) == param
                    ? otherwise
                    : this[name](param, this.options)
                : otherwise
        },
    },
}

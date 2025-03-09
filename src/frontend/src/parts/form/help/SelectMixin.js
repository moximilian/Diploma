import SelectPropsMixin from './props/SelectPropsMixin'
import SelectFormatMixin from './SelectFormatMixin'
import SelectPositionMixin from './SelectPositionMixin'
export default {
    mixins: [SelectPropsMixin, SelectFormatMixin, SelectPositionMixin],
    data() {
        return {
            selected: {},
            searchValue: '',
            searching: false,
            isEscAvailable: true,
            isArray: false,
        }
    },
    watch: {
        value() {
            this.setDefault()
        },
        search() {
            this.searchValue = this.search
        },
        options() {
            if (Object.isEmpty(this.selected)) this.setDefault()
        },
    },
    computed: {
        emptyOptions() {
            return this.type !== 'search' && this.isEmpty(this.options)
        },
        optionList() {
            if (!this.searchValue || !this.isLocalSearch) return this.options
            const searching = val =>
                String(this.showValue(val)).toLowerCase().includes(this.searchValue.toLowerCase())

            return this.isArray
                ? this.options.filter(searching)
                : Object.fromEntries(
                      Object.entries(this.options).filter(([, val]) => searching(val))
                  )
        },
        realValue() {
            if (this.isEmpty(this.selected)) return null
            let selected = Object[this.isArray ? 'values' : 'keys'](this.selected).map(selection =>
                this.checkFunction('outFormat', selection, this.getKey(selection))
            )

            return !this.multiple ? selected[0] : selected
        },
        viewSelected() {
            return Object.values(this.selected).map(this.showValue)
        },
        preparedPlaceholder() {
            // return this.$t('forms.fields.choose_from_list')
            return 'Выберете из списка'
        },
    },
    methods: {
        optionKey(key, val) {
            if (arguments.length < 2) return arguments[0]
            return this.getKey(this.isArray ? val : key)
        },
        onChange(key, val) {
            val = this.optionKey(...arguments)
            this.searchValue = ''
            if (this.isDisabled(key)) return
            if (this.isSelected(val)) return this.unSelect(val)
            if (
                'function' === typeof this.beforeSet &&
                !this.beforeSet(val, this.realValue, this.selected, this.options)
            )
                return

            if (!this.multiple) this.clear(false)
            this.select(val)
            this.changeValue()
        },
        isDisabled(key) {
            return Array.isArray(this.disabledOptions) ? this.disabledOptions[key] : this.disabled
        },
        select(key, val) {
            val = this.optionKey(...arguments)
            if (!this.multiple) this.selected = {}
            if (this.isArray)
                this.options.forEach(opt => val === this.getKey(opt) && (this.selected[val] = opt))
            else this.selected[val] = this.options[val]
            this.$emit('select', this.selected[val])
        },
        unSelect(key, val) {
            val = this.optionKey(...arguments)
            if (!this.isEmptyAvailable && Object.keys(this.selected).length === 1) return
            delete this.selected[val]
            this.changeValue()
            this.$emit('unSelect', val)
        },
        onSearch(value) {
            !this.opened && this.open?.()
            this.searchValue = value
            this.$emit('search', this.searchValue)
            if (this.type !== 'search') this.isEscAvailable = Boolean(!this.searchValue)
        },
        clear(emited = true) {
            this.selected = {}
            emited && this.changeValue()
        },
        setDefault() {
            if (this.isEmpty(this.value)) {
                this.clear(false)
                return
            }

            let values = Array.isArray(this.value) ? this.value : [this.value]
            if (!this.multiple) values = [values[0]]
            values.forEach(val => this.select(this.getKey(val)))
        },
        getValue(val) {
            if ('object' === typeof val) return val?.text || val.value || val[Object.keys(val)[0]]
            return val
        },
        isSelected(key, val) {
            val = this.optionKey(...arguments)
            return Object.keys(this.selected).includes(`${val}`)
        },
        isEmpty(param) {
            if (['number', 'string'].includes(typeof param)) return false
            if ('object' === typeof param) {
                if (Array.isArray(param)) return param.length === 0
                for (const prop in param) {
                    if (Object.hasOwn(param, prop)) return false
                }
            }
            return true
        },
        changeValue() {
            this.$emit('changeValue', this.realValue, this.name)
        },
    },
    created() {
        this.searchValue = this.search
        this.isArray = Array.isArray(this.options)
        this.setDefault()
    },
}

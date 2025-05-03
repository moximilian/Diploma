import SelectFormatMixin from './SelectFormatMixin'
export default {
    props: {
        modelName: { type: String, default: null },
        groups: { type: Array, default: null },
        groupFields: { type: Array, default: null },
        defaultWheres: { type: Array, default: () => [] },
        fieldKey: { type: String, default: null },
        showFieldName: { type: String, default: () => 'name' },
        searchField: { type: [String, Array], default: null },
        defaultLimit: { type: Number, default: () => 15 },
        afterFetch: { type: Function, default: null },
        isBaseRequestAllowed: { type: Boolean, default: () => true },
        emptyValue: { type: String, default: () => '—' },
        isLocalSearch: { type: Boolean, default: () => false },
    },
    emits: ['loaded'],
    mixins: [SelectFormatMixin],
    data() {
        return {
            searchValue: null,
            isLoading: true,
            optionRows: [],
        }
    },
    computed: {
        model() {
            return this.$api[this.modelName]
        },
        keyColumn() {
            return this.groups ? this.groups?.[0]?.column : this.fieldKey
        },
        searchColumn() {
            return this.searchField || this.showFieldName || this.keyColumn
        },
        wheres() {
            if (
                this.searchValue === null &&
                ![null, undefined, ''].includes(this.value) &&
                (!Array.isArray(this.value) || this.value.length) &&
                this.isBaseRequestAllowed
            ) {
                const value = [this.value].flat()
                return [
                    ...this.defaultWheres,
                    {
                        column: this.keyColumn,
                        condition: 'in',
                        value: value.map(item => this.getKey(item)),
                    },
                ]
            }

            if (this.isSearch && this.searchValue)
                return [
                    ...this.defaultWheres,
                    {
                        column: this.searchColumn,
                        condition: '%',
                        value: this.searchValue?.trim(),
                    },
                ]

            return this.defaultWheres
        },
        fetchOptions() {
            return {
                filters: {
                    wheres: this.wheres,
                    groups: this.groups ? { groups: this.groups, fields: this.groupFields } : null,
                },
                page: 1,
                limit: this.defaultLimit,
            }
        },
    },
    methods: {
        async load() {
            this.isLoading = true
            const { body } = await this.model.list(this.fetchOptions)
            this.optionRows = body.rows
        },
    },
}

import SelectPropsMixin from './props/SelectPropsMixin'
import OptionModelMixin from './OptionModelMixin'
export default {
    mixins: [SelectPropsMixin, OptionModelMixin],
    watch: {
        searchValue(newSearch) {
            newSearch === '' && this.load()
        },
    },
    computed: {
        isSearch() {
            return this.type === 'search'
        },
    },
    methods: {
        searchCb(search) {
            if (!this.isSearch || this.isLocalSearch) return

            this.searchValue = search
            if (search?.length > 1) {
                this.load()
                this.$emit('search', search)
            }
        },
        opened() {
            this.searchValue = ''
            this.load()
            this.$emit('onOpened')
        },
        closed() {
            this.searchValue = ''
            this.$emit('onClosed')
        },
    },
    provide() {
        return {
            modelName: this.modelName,
        }
    },
    created() {
        if (!this.modelName) {
            console.error('DropDownModel: Model Name does not exists')
            return
        }
        if (!this.model) {
            console.error(`DropDownModel: Model ${this.modelName} does not exists`)
            return
        }
        this.load()
    },
}

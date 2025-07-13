import SelectPropsMixin from './props/SelectPropsMixin'
import OptionModelMixin from './OptionModelMixin'
export default {
    mixins: [SelectPropsMixin, OptionModelMixin],
    watch: {
        async searchValue(newSearch) {
            newSearch === '' && (await this.load())
        },
    },
    computed: {
        isSearch() {
            return this.type === 'search'
        },
    },
    methods: {
        async searchCb(search) {
            if (!this.isSearch || this.isLocalSearch) return

            this.searchValue = search
            if (search?.length > 1) {
                await this.load()
                this.$emit('search', search)
            }
        },
        async opened() {
            this.searchValue = ''
            await this.load()
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
    async created() {
        if (!this.modelName) {
            console.error('DropDownModel: Model Name does not exists')
            return
        }
        if (!this.model) {
            console.error(`DropDownModel: Model ${this.modelName} does not exists`)
            return
        }
        await this.load()
    },
}

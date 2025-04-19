export default {
    computed: {
        queryTab() {
            return this.$route.query?.tab ?? this.selectedOption
        },
    },
    data() {
        return {
            selectedOption: ''
        }
    },
    methods: {
        select(option) {
            this.$router.push(`${this.$route.path}?tab=${option}`)
        },
        isSelected(option) {
            return this.selectedOption === option
        },
    },
    watch: {
        queryTab() {
            this.selectedOption = this.queryTab
        },
    },
    created() {
        this.selectedOption = this.queryTab
    },
}

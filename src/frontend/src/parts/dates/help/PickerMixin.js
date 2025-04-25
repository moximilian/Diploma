import mitt from 'mitt'
import { addGroupEventListeners } from '@/core/functions'
const emitter = mitt()

export default {
    props: {
        disabled: { type: Boolean, default: () => false },
    },
    emits: ['changeValue'],
    provide() {
        return {
            setChildOpened: value => {
                if (value) this.childOpened++
                else this.childOpened--
            },
        }
    },
    data() {
        return {
            opened: false,
            childOpened: 0,
            selectedDates: [],
            stateDate: null,
            current: null,
        }
    },
    watch: {
        value() {
            !this.opened && this.setDefault()
        },
    },
    computed: {
        stopMonth() {
            return {
                y: this.current.getFullYear(),
                m: this.current.getMonth(),
            }
        },
    },
    methods: {
        close() {
            this.opened = false
        },
        toggle() {
            this.opened = !this.opened
        },

        prevMonth() {
            this.current.setMonth(this.current.getMonth() - 1)
            this.current = new Date(this.current)
        },
        nextMonth() {
            this.current.setMonth(this.current.getMonth() + 1)
            this.current = new Date(this.current)
        },
        setMonth(year, month) {
            this.current.setFullYear(year, month)
            this.current = new Date(this.current)
        },
        setDefault() {
            if (Array.isArray(this.value))
                return this.value.map((val, i) => val && (this.selectedDates[i] = new Date(val)))
            if (this.value) {
                const value = this.value.split('-').reverse().join('-')
                return this.selectedDates.push(new Date(value))
            }
            this.selectedDates = []
        },
        changeValue(value, name) {
            this.$emit('changeValue', value, name)
        },
        selectedDateEmit() {
            this.setDateToLS()
            this.$emit('changeValue', this.giveDates(), this.name)
        },
        getCurrentValue() {
            if (this.value instanceof Date) return this.value
            if (typeof this.value === 'string' && this.value.trim()) {
                const value = this.value.split('-').reverse().join('-')
                return new Date(value)
            }
            return new Date()
        },
    },
    mounted() {
        emitter.on(
            'hook:beforeDestroy',
            addGroupEventListeners(document, {
                click: e => this.opened && !this.$el.contains(e.target) && this.close(e),
                keydown: e => e.code === 'Escape' && this.close(e),
            }).abort
        )
    },
    created() {
        this.current = this.getCurrentValue()
        this.setDefault()
    },
}

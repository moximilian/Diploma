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
            if (this.value) return this.selectedDates.push(new Date(this.value))
            this.selectedDates = []
        },
        changeValue(value) {
            this.$emit('changeValue', value)
        },
        selectedDateEmit() {
            this.setDateToLS()
            this.$emit('changeValue', this.giveDates())
        },
        getCurrentValue() {
            if (this.value instanceof Date) return this.value
            if (typeof this.value === 'string' && this.value.trim()) return new Date(this.value)
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

<template>
    <div class="time-value-select">
        <div class="time-value-select-item">
            <th
                class="calendar-nav time-picker-nav"
                @click="hours++"
                @mousedown="fastChange(() => hours++)"
                @mouseup="fastChange(false)"
                @mouseleave="fastChange(false)"
            >
                <i class="fas fa-chevron-up"></i>
            </th>
            <div class="time-picker-value">
                {{ hours }}
            </div>
            <th
                class="calendar-nav time-picker-nav"
                @click="hours--"
                @mousedown="fastChange(() => hours--)"
                @mouseup="fastChange(false)"
                @mouseleave="fastChange(false)"
            >
                <i class="fas fa-chevron-down"></i>
            </th>
        </div>

        <div class="time-value-select-item">
            <th
                class="calendar-nav time-picker-nav"
                @click="minutes++"
                @mousedown="fastChange(() => minutes++)"
                @mouseup="fastChange(false)"
                @mouseleave="fastChange(false)"
            >
                <i class="fas fa-chevron-up"></i>
            </th>
            <div class="time-picker-value">
                {{ minutes }}
            </div>
            <th
                class="calendar-nav time-picker-nav"
                @click="minutes--"
                @mousedown="fastChange(() => minutes--)"
                @mouseup="fastChange(false)"
                @mouseleave="fastChange(false)"
            >
                <i class="fas fa-chevron-down"></i>
            </th>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        value: { type: String, default: '' },
        name: { type: String, default: null },
    },

    data() {
        return {
            hours: this.value.split(':')[0],
            minutes: this.value.split(':')[1],
            timeout: '',
            interval: '',
        }
    },

    watch: {
        hours() {
            this.normalizeValue('hours', 23)
        },

        minutes() {
            this.normalizeValue('minutes', 59)
        },

        value() {
            [this.hours, this.minutes] = this.value.split(':')
        },
    },

    computed: {
        realValue() {
            return `${this.hours}:${this.minutes}`
        },
    },

    methods: {
        fastChange(action) {
            if (!action) {
                clearTimeout(this.timeout)
                clearInterval(this.interval)
                return
            }
            clearTimeout(this.timeout)
            this.timeout = setTimeout(() => {
                this.interval = setInterval(() => action(), 90)
            }, 450)
        },

        normalizeValue(type, max) {
            if (this[type].toString().length === 1) this[type] = `0${this[type]}`
            if (this[type] > max) this[type] = '00'
            if (this[type] < 0) this[type] = max
            this.$emit('change', this.realValue, this.name)
        },
    },
}
</script>

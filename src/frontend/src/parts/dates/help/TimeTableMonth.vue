<template>
    <table class="calendar-timetable" :class="calendarClass">
        <tbody>
            <tr>
                <th v-for="(wday, i) in wdays" :key="wday" :class="{ weekend: isWeekend(i) }">
                    {{ wday }}
                </th>
            </tr>
            <tr v-for="(week, i) in currentMonthDays" :key="i">
                <td v-for="d in week" :key="d.date" v-bind="isShowTitle(d.date)">
                    <div :class="dayClass(d)" class="date-timetable">
                        {{ d.day }}
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import MonthHelper from './MonthHelper'

export default {
    mixins: [MonthHelper],
    props: {
        current: {
            type: Object,
            default: () => {
                const n = new Date()
                return { y: n.getFullYear(), m: n.getMonth() }
            },
        },
        selectedDates: { type: Array, default: () => [] },
        datetime: { type: Date, default: null },
        selectedDateState: { type: Boolean, default: null },
        maxShowDate: { type: Date, default: null },
        minShowDate: { type: Date, default: null },
        maxSelectDays: { type: Number, default: null },
    },
    computed: {
        calendarClass() {
            return this.selectedDates.length > 1 &&
                !this.selectedDates[0].isEquals(this.selectedDates[1])
                ? ' rangeSelected'
                : ''
        },
        dateShown() {
            return this.datetime ? this.datetime.toShowDate() : ''
        },
    },
    methods: {
        prevMonth() {
            this.$emit('prevMonth')
        },
        nextMonth() {
            this.$emit('nextMonth')
        },
        setMonth(year, month) {
            this.$emit('setMonth', year, month)
        },
        selectDate(date, type) {
            if (this.isDateDisabled(date)) {
                return
            }
            this.$emit('selectDate', date, type)
        },
        setTime(time) {
            this.$emit('setTime', time)
        },
        changeInput(date) {
            this.$emit('changeInput', date)
        },
        dateFocusStatus(status) {
            this.$emit('dateFocusStatus', status)
        },
    },
}
</script>

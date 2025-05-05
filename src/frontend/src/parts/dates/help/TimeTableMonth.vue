<template>
    <table v-if="isShow" class="calendar-timetable" :class="calendarClass">
        <tbody>
            <tr>
                <th v-for="(wday, i) in wdays" :key="wday" :class="{ weekend: isWeekend(i) }">
                    {{ wday }}
                </th>
            </tr>
            <tr v-for="(week, i) in currentMonthDays" :key="i">
                <td v-for="d in week" :key="d.date" v-bind="isShowTitle(d.date)">
                    <div class="table-month-day">
                        <div :class="dayClass(d)" class="date-timetable">
                            {{ d.day }}
                        </div>
                        <div
                            class="event"
                            v-for="event in getEventsByDate(d)"
                            :key="event.id"
                            @click="$router.push('/events/show/' + event.id)"
                        >
                            {{ event?.name }}
                        </div>
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
        isShow: { type: Boolean, default: () => false },
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
        events: { type: Array, default: () => [] },
    },
    // data() {
    //     return {
    //         blocksColors: ['var(--main-color)', 'pink', 'blue', 'violed', 'green'],
    //     }
    // },
    computed: {
        eventsDates() {
            return this.events.reduce((events, event) => {
                event.start_date = event.start_date.split('T')[0]
                return events
            }, this.events)
        },
        calendarClass() {
            return this.selectedDates.length > 1 &&
                !this.selectedDates[0].isEquals(this.selectedDates[1])
                ? ' rangeSelected'
                : ''
        },
        dateShown() {
            return this.datetime ? this.datetime.toShowDate() : ''
        },
        monthActiveDays() {
            return this.currentMonthDays
                .flat()
                .filter(day => !day.class.includes('unactive'))
                .map(day => new Date(day.date))
        },
    },
    methods: {
        getEventsByDate(day) {
            return this.eventsDates.filter(event => event.start_date === day.date)
        },
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
        firstLastDaysMonth() {
            return [this.monthActiveDays[0], this.monthActiveDays.at(-1)]
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

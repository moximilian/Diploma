<template>
    <div class="timetable-week border">
        <div v-for="(day, index) of currentWeek" :key="index" class="timetable-day">
            <div class="flex-container-column" :style="{ marginBottom: '20px' }">
                <div>{{ wdays[index] }}</div>
                <div>{{ day.date.split('-')[2] }}</div>
            </div>
            <TimeTableDay
                :currentDay="new Date(day.date)"
                :viewHours="index == 0"
                class="border-right"
            />
        </div>
    </div>
</template>
<script>
import TimeTableDay from './TimeTableDay.vue'
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
    data() {
        return {
            currentWeekIndex: 0,
        }
    },
    watch: {
        currentDateShow() {
            this.getCurrentWeekIndex()
        },
    },
    computed: {
        currentDateShow() {
            return this.selectedDates[0].toShowDate(false)
        },
        currentWeek() {
            return this.currentMonthDays[this.currentWeekIndex]
        },
    },
    methods: {
        getCurrentWeekIndex() {
            let foundIndex = null
            this.currentMonthDays.forEach((week, index) => {
                week.forEach(day => {
                    if (day.date === this.currentDateShow && foundIndex === null) {
                        foundIndex = index
                    }
                })
            })
            this.currentWeekIndex = foundIndex
        },
    },
    created() {
        this.getCurrentWeekIndex()
    },
    components: {
        TimeTableDay,
    },
}
</script>

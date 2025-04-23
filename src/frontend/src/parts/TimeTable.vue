<template>
    <NestedPage :title="currentDateLabel">
        <template #page-header-right>
            <div :class="{ selected: isSelected('today') }" @click="selectToday()">Сегодня</div>
            <div :class="{ selected: isSelected('day') }" @click="select('day')">День</div>
            <div :class="{ selected: isSelected('week') }" @click="select('week')">Неделя</div>
            <div :class="{ selected: isSelected('month') }" @click="select('month')">Месяц</div>
            <div class="flex-container-row">
                <BaseBtn class="small" :outline="true" @click="prev()">{{ '<' }}</BaseBtn>
                <BaseBtn class="small" :outline="true" @click="next()">{{ '>' }}</BaseBtn>
            </div>
        </template>
        <template #page-content>
            <div class="flex-container-row flex-start timetable-layout">
                <DateCalendar
                    :current="stopMonth"
                    :selectedDates="selectedDates"
                    :minShowDate="min"
                    :maxShowDate="max"
                    @selectDate="selectDate"
                    @prevMonth="prevMonth"
                    @nextMonth="nextMonth"
                    @setMonth="setMonth"
                />
                <TimeTableMonth
                    v-if="isSelected('month')"
                    :current="stopMonth"
                    ref="month"
                    :selectedDates="selectedDates"
                    :minShowDate="min"
                    :maxShowDate="max"
                />
                <TimeTableDay v-if="isSelected('today')" :currentDay="new Date()" class="border" />
                <TimeTableDay
                    v-if="isSelected('day')"
                    :currentDay="selectedDates[0]"
                    class="border"
                />
                <TimeTableWeek
                    v-if="isSelected('week')"
                    :current="stopMonth"
                    ref="week"
                    :selectedDates="selectedDates"
                />
            </div>
        </template>
    </NestedPage>
</template>

<script>
import DateCalendar from '@/parts/dates/help/DateCalendar'
import PickerMixin from '@/parts/dates/help/PickerMixin'
import MonthHelper from '@/parts/dates/help/MonthHelper'
import TimeTableMonth from '@/parts/dates/help/TimeTableMonth'
import TimeTableDay from '@/parts/dates/help/TimeTableDay'
import TimeTableWeek from '@/parts/dates/help/TimeTableWeek'

import TabsMixin from '@/pages/_help/TabsMixin'

export default {
    mixins: [PickerMixin, TabsMixin, MonthHelper],
    data() {
        return {
            childOpened: 0,
            selectedDates: [],
            stateDate: null,
            current: null,
            min: null,
            max: null,

            monthsLabelsChanged: [
                'января',
                'февраля',
                'марта',
                'апреля',
                'мая',
                'июня',
                'июля',
                'августа',
                'сентебря',
                'октября',
                'ноября',
                'декабря',
            ],
            monthsLabels: [
                'Январь',
                'Февраль',
                'Март',
                'Апрель',
                'Май',
                'Июнь',
                'Июль',
                'Август',
                'Сентябрь',
                'Октябрь',
                'Ноябрь',
                'Декабрь',
            ],
            daysToChange: {
                week: 7,
                month: 30,
                day: 1,
                today: 0,
            },
        }
    },
    watch: {
        wheres: {
            handler() {
                this.fetchEvents()
            },
            deep: true,
        },
    },
    computed: {
        currentDateLabel() {
            const date = this.selectedDates[0] ?? new Date()

            return ['today', 'day'].includes(this.selectedOption)
                ? `${date.getDate()} ${
                      this.monthsLabelsChanged[date.getMonth()]
                  } ${date.getFullYear()}`
                : `${this.monthsLabels[this.stopMonth?.m ?? 0]} ${this.stopMonth?.y ?? 0}`
        },
        isStudent() {
            return this.$store.getters.isStudent
        },
        wheres() {
            return {
                today: [{
                    column: 'start_date',
                    condition: '=',
                    value: new Date()
                }],
                day: [{
                    column: 'start_date',
                    condition: '=',
                    value: new Date(this.stateDate)
                }],
                week: this.$refs?.week?.firstLastDaysWeek() ? [{
                    column: 'start_date',
                    condition: 'between',
                    value: this.$refs?.week?.firstLastDaysWeek()
                }] : [],
                month: this.$refs?.month?.firstLastDaysMonth() ? [{
                    column: 'start_date',
                    condition: 'between',
                    value: this.$refs?.month?.firstLastDaysMonth()
                }] : [],
            }?.[this.selectedOption] ?? []
        }
    },
    methods: {
        selectDate(date) {
            if (date) {
                let d1 = new Date(date),
                    d2 = new Date(date)
                d1.setHours(0, 0, 0)
                d2.setHours(23, 59, 59)
                // this.selectedDates = [d1, d2]
                this.selectedDates = [d1]
            } else {
                this.selectedDates = []
            }
            if (date !== new Date() && this.isSelected('today')) {
                this.select('day')
            }

            if (this.stateDate !== date) {
                this.stateDate = date
                this.changeValue(date)
                setTimeout(() => this.close(), 200)
            }
        },
        adjustDateByWeek(originalDate, daysTo = 7, isAdd = true) {
            const newDate = new Date(originalDate)
            isAdd
                ? newDate.setDate(originalDate.getDate() + daysTo)
                : newDate.setDate(originalDate.getDate() - daysTo)
            if (this.selectedDates[0].getMonth() !== newDate.getMonth())
                isAdd ? this.nextMonth() : this.prevMonth()
            this.selectDate(newDate)
        },
        prev() {
            this.adjustDateByWeek(
                this.selectedDates[0],
                this.daysToChange[this.selectedOption],
                false
            )
        },
        next() {
            this.adjustDateByWeek(
                this.selectedDates[0],
                this.daysToChange[this.selectedOption],
                true
            )
        },
        selectToday() {
            this.selectDate(new Date())
            this.select('today')
        },
        fetchEvents() {
            this.$api.events.list({
            filters: {
                wheres: [
                    {
                        column: 'role',
                        value: {
                            [true]: 'student',
                            [false]: 'teacher',
                        }[this.isStudent],
                    },
                    ...this.wheres
                ],
            },
        }, (res) => {
            console.log('events', {res})
        })
        }
    },
    created() {
        this.selectToday()
        this.fetchEvents()
    },
    components: {
        DateCalendar,
        TimeTableMonth,
        TimeTableDay,
        TimeTableWeek,
    },
}
</script>

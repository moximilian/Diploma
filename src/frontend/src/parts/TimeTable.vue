<template>
    <NestedPage :title="currentDateLabel">
        <template #page-header-right>
            <div :class="{ selected: isSelected('today') }" @click="selectToday()">Сегодня</div>
            <div :class="{ selected: isSelected('day') }" @click="select('day', dateWheres)">
                День
            </div>
            <div :class="{ selected: isSelected('week') }" @click="selectTab('week')">Неделя</div>
            <div :class="{ selected: isSelected('month') }" @click="selectTab('month')">Месяц</div>
            <div class="flex-container-row">
                <BaseBtn class="small" :outline="true" @click="prev()">{{ '<' }}</BaseBtn>
                <BaseBtn class="small" :outline="true" @click="next()">{{ '>' }}</BaseBtn>
            </div>
        </template>
        <template #page-content>
            <div class="flex-container-row flex-start timetable-layout">
                <div class="flex-container-column timetable-left">
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
                    <BaseBtn
                        v-if="!isStudent"
                        value="Добавить слот"
                        @click="$router.push('/slots/new')"
                    />
                    <div class="page-content-filter" v-if="isStudent">
                        <FilterForm filterName="slotsStudent" @changeFilters="changeFilters" />
                    </div>
                </div>
                <TimeTableMonth
                    :isShow="isSelected('month')"
                    :current="stopMonth"
                    ref="month"
                    :selectedDates="selectedDates"
                    :minShowDate="min"
                    :maxShowDate="max"
                    :events="uniqueEvents"
                />

                <TimeTableDay
                    :isShow="isSelected('today')"
                    :currentDay="new Date()"
                    class="border"
                    :events="uniqueEvents"
                />
                <TimeTableDay
                    :isShow="isSelected('day')"
                    :currentDay="selectedDates[0]"
                    class="border"
                    :events="uniqueEvents"
                />
                <TimeTableWeek
                    :isShow="isSelected('week')"
                    :current="stopMonth"
                    ref="week"
                    :selectedDates="selectedDates"
                    :events="uniqueEvents"
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
            isLoading: false,
            eventsFilters: [],
            slotsFilters: [],
            events: [],

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
        dateWheres: {
            handler() {
                this.fetchEvents()
            },
            deep: true,
        },
    },
    computed: {
        uniqueEvents() {
            return [...new Map(this.events.map(item => [item.id, item])).values()]
        },
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
        toDate(date) {
            return new Date(date)
        },
        dateWheres() {
            return (
                {
                    today: [
                        {
                            column: 'start_date',
                            condition: 'between',
                            value: [
                                new Date(new Date().setHours(0, 0, 0)),
                                new Date(new Date().setHours(23, 59, 59)),
                            ],
                        },
                    ],
                    day: [
                        {
                            column: 'start_date',
                            condition: 'between',
                            value: [
                                new Date(new Date(this.stateDate).setHours(0, 0, 0)),
                                new Date(new Date(this.stateDate).setHours(23, 59, 59)),
                            ],
                        },
                    ],
                    week: this.getWeekFilter(),
                    month: this.$refs?.month?.firstLastDaysMonth()
                        ? [
                              {
                                  column: 'start_date',
                                  condition: 'between',
                                  value: this.$refs?.month?.firstLastDaysMonth(),
                              },
                          ]
                        : [],
                }?.[this.selectedOption] ?? []
            )
        },
    },
    methods: {
        getWeekFilter() {
            const weekEl = this.$refs?.week
            if (!weekEl) return []
            return [
                {
                    column: 'start_date',
                    condition: 'between',
                    value: weekEl.firstLastDaysWeek(),
                },
            ]
        },
        changeFilters(wheres) {
            this.slotsFilters = wheres.filter(where => where.column == 'creator_id') ?? []
            this.eventsFilters = wheres.filter(where => where.column == 'group_id') ?? []
            this.fetchEvents()
        },
        selectTab(tab) {
            this.select(tab, this.dateWheres)
            this.fetchEvents()
        },
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
        adjustDate(originalDate, daysTo = 7, isAdd = true) {
            const newDate = new Date(originalDate)
            isAdd
                ? newDate.setDate(originalDate.getDate() + daysTo)
                : newDate.setDate(originalDate.getDate() - daysTo)
            if (this.selectedDates[0].getMonth() !== newDate.getMonth())
                isAdd ? this.nextMonth() : this.prevMonth()
            this.selectDate(newDate)
        },
        prev() {
            this.adjustDate(this.selectedDates[0], this.daysToChange[this.selectedOption], false)
        },
        next() {
            this.adjustDate(this.selectedDates[0], this.daysToChange[this.selectedOption], true)
        },
        selectToday() {
            this.selectDate(new Date())
            this.select('today', this.dateWheres)
        },
        async fetchEvents() {
            this.events = []
            this.isLoading = true
            if (Array.isEmpty(this.dateWheres)) return
            const filters = {
                filters: {
                    wheres: [
                        {
                            column: 'role',
                            value: {
                                [true]: 'student',
                                [false]: 'teacher',
                            }[this.isStudent],
                        },
                        ...this.dateWheres,
                        ...this.eventsFilters,
                    ],
                },
            }
            const { body } = await this.$api.events.list(filters)
            this.events.push(
                ...body.rows?.sort((first, second) =>
                    first.start_time > second.start_time ? 1 : -1
                )
            )
            const res = await this.$api.slots.list({
                filters: {
                    wheres: [
                        ...(!this.isStudent ? [{ column: 'role', value: 'teacher' }] : []),
                        ...this.dateWheres,
                        ...this.slotsFilters,
                    ],
                },
            })
            this.events.push(
                ...res.body.rows?.sort((first, second) =>
                    first.start_time > second.start_time ? 1 : -1
                )
            )
            this.isLoading = false
        },
    },
    async created() {
        this.selectToday()
        await this.fetchEvents()
    },
    components: {
        DateCalendar,
        TimeTableMonth,
        TimeTableDay,
        TimeTableWeek,
    },
}
</script>

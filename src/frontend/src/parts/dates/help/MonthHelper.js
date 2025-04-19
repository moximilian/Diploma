export default {
    data() {
        return {
            wdays: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
        }
    },
    emits: [
        'prevMonth',
        'nextMonth',
        'setMonth',
        'selectDate',
        'setTime',
        'dateFocusStatus',
        'changeInput',
    ],
    computed: {
        langOffset() {
            // return ['en'].includes(this.$i18n.locale) ? 0 : -1
            return -1
        },
        currentMonthDays() {
            const dateIterator = new Date(this.current.y, this.current.m, 1)
            const firstWday = (dateIterator.getDay() + this.langOffset + 7) % 7
            dateIterator.setDate(dateIterator.getDate() - firstWday)

            const daysByWeek = []
            for (let i = 0; i < 6; i++) {
                const daysLine = []
                for (let j = 0; j < 7; j++) {
                    let className =
                        dateIterator.getMonth() === this.current.m ? 'active' : 'unactive'
                    if (this.isToday(dateIterator)) className += ' today'
                    if (this.isWeekend(j)) className += ' weekend'

                    if (this.inSelectedDates(dateIterator)) {
                        className +=
                            typeof this.selectedDateState !== 'object' &&
                            dateIterator.isEquals(
                                this.selectedDates[this.selectedDateState ? 0 : 1]
                            )
                                ? ' included-stripes'
                                : ' selected'
                    } else if (this.inSelectedRange(dateIterator)) {
                        className += ' included'
                    }
                    daysLine.push({
                        class: className,
                        date: dateIterator.toShowDate(false),
                        day: dateIterator.getDate(),
                    })
                    dateIterator.setDate(dateIterator.getDate() + 1)
                }
                daysByWeek.push(daysLine)
            }
            return daysByWeek
        },
    },
    methods: {
        dayClass(dayObject) {
            const currClass = dayObject.class
            const isDisabled = this.isDateDisabled(dayObject.date)
            return isDisabled
                ? currClass.replace('unactive', 'disabled').replace('active', 'disabled')
                : currClass
        },
        isDateDisabled(date) {
            if ((!this.minShowDate && !this.maxShowDate) || this.selectedDateState) return false
            return (
                this.minShowDate?.getTime() >= new Date(date).getTime() ||
                this.maxShowDate?.getTime() <= new Date(date).getTime()
            )
        },
        isShowTitle(date) {
            if (this.isDateDisabled(date)) {
                return {
                    title: this.getWarnMessage(),
                }
            }
        },
        isToday(d) {
            return new Date().isEquals(d)
        },
        isWeekend(value) {
            return [0, 6].includes((value - this.langOffset) % 7)
        },
        inSelectedDates(date) {
            return this.selectedDates && this.inDates(date, this.selectedDates)
        },
        inSelectedRange(date) {
            return this.selectedDates && this.inDatesRange(date, this.selectedDates)
        },
        inDates(d1, d2s) {
            for (let d2 of d2s) {
                if (d1.isEquals(d2)) return true
            }
            return false
        },
        inDatesRange(d1, range) {
            const start = range[0] && d1.getTime() >= range[0].getTime()
            const stop = range[1] && d1.getTime() <= range[1].getTime()
            return start && stop
        },
    },
}

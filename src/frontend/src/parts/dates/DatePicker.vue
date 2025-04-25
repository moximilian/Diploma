<template>
    <div class="field fieldDate" :class="{ disabled, opened }">
        <slot name="beforeInput"></slot>
        <StringField
            ref="field"
            :value="date"
            :disabled="disabled"
            :readonly="true"
            :placeholder="$t(placeholder)"
            @click="toggle"
        >
            <template v-slot:beforeInput="{ focused }">
                <i class="icon icon-scheduler" :class="{ active: focused }" @click="focus"></i>
            </template>
        </StringField>
        <DateCalendar
            v-if="opened"
            class="field-dropdown"
            :current="stopMonth"
            :selectedDates="selectedDates"
            :minShowDate="min"
            :maxShowDate="max"
            @selectDate="selectDate"
            @prevMonth="prevMonth"
            @nextMonth="nextMonth"
            @setMonth="setMonth"
        />
    </div>
</template>

<script>
import DateCalendar from './help/DateCalendar.vue'
import PickerMixin from './help/PickerMixin.js'

export default {
    mixins: [PickerMixin],
    props: {
        value: { type: [Array, String, Date], default: null },
        name: { type: String, default: () => '' },
        placeholder: { type: String, default: () => 'Выберите дату' },
        min: { type: [Array, String, Date], default: null },
        max: { type: [Array, String, Date], default: null },
    },
    computed: {
        date() {
            return this.selectedDates[0] ? this.selectedDates[0].toShowDate() : ''
        },
    },
    methods: {
        focus() {
            this.field?.focus()
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

            if (this.stateDate !== date) {
                this.stateDate = date
                this.changeValue(date)
                setTimeout(() => this.close(), 200)
            }
            this.$emit('changeValue', this.date, this.name)
        },
    },
    components: { DateCalendar },
}
</script>

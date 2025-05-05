<template>
    <slot name="beforeInput" v-bind="$props"></slot>
    <div>
        <div>
            <InputField
                ref="input"
                class="timePicker"
                :value="realValue"
                @click="toggle"
                readonly
                @changeValue="onChange"
            />
        </div>
        <div v-if="opened" class="field-dropdown time-picker">
            <SelectTimeField :value="realValue" @change="onChange" />
        </div>
    </div>
</template>

<script>
export default {
    props: {
        value: { type: [Date, String], default: null },
        
        name: { type: String, default: () => '' },
    },
    emits: ['changeValue', 'dateFocusStatus'],
    data() {
        return {
            opened: false,
            timeValue: this.value,
        }
    },

    computed: {
        realValue() {
            return this.prepareValue(this.timeValue)
        },
    },

    methods: {
        prepareValue(value) {
            if (!value) return '00:00'
            return value instanceof Date
                ? value.toShowTime()
                : value
                      .toString()
                      .split(':')
                      .map(part => part.padStart(2, '0'))
                      .join(':')
        },

        normalizeTime(time) {
            return /^([0-1]?[0-9]|2[0-4]):([0-5][0-9])(:[0-5][0-9])?$/.test(time)
                ? time
                : this.realValue
        },

        onChange(event) {
            let value = event?.target?.value || event
            const normalizedTime = this.normalizeTime(value)
            this.timeValue = normalizedTime
            this.$emit('changeValue', normalizedTime, this.name)
        },

        toggle() {
            this.opened = !this.opened
            console.log(this.opened)
        },
    },
}
</script>

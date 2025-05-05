<template>
    <slot name="beforeInput" v-bind="$props"></slot>
    <InputField 
        v-bind="computedProps"
        @onBlur="onBlur"
        @changeValue="changeValue"
    />
</template>

<script>
import InputPropsMixin from './help/props/InputPorpsMixin'
export default {
    mixins: [InputPropsMixin],
    computed: {
        computedProps() {
            let result = Object.fromEntries(Object.entries(this.$props))
            result.afterInputFormat = this.$props.afterInputFormat || this.transformNumberInput
            result.type = 'number'
            return result
        }
    },
    methods: {
        transformNumberInput(value) {
            const min = this.$props.min || 0
            const max = this.$props.max || value
            if (!value || value < min) return min
            if (value > max) return max
            return value
        },
        onBlur() {
            this.$emit('onBlur')
        },
        changeValue(value, name) {
            this.$emit('changeValue', value, name)
        }
    },
}
</script>

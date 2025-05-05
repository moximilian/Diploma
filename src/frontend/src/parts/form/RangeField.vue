<template>
    <div class="range-field">
        <slot name="beforeInput"> </slot>
        <div class="inputs">
            <NumberField
                name="min"
                :value="realValue[0]"
                placeholder="от"
                maxlength="64"
                @changeValue="value => setValue(value, 'min')"
            />
            -
            <NumberField
                name="max"
                placeholder="до"
                :value="realValue[1]"
                maxlength="64"
                @changeValue="value => setValue(value, 'max')"
            />
        </div>
    </div>
</template>

<script>
import InputPropsMixin from './help/props/InputPorpsMixin'

export default {
    mixins: [InputPropsMixin],
    emits: ['changeValue'],
    data() {
        return {
            minValue: this.value[0] > 0 ? this.value[0] : 0,
            maxValue: this.value[1] > 0 ? this.value[1] : 0,
        }
    },
    computed: {
        realValue() {
            return [this.minValue, this.maxValue]
        },
    },
    methods: {
        setValue(value, type) {
            this[`${type}Value`] = value
            if (this.realValue[0] !== null && this.realValue !== null) {
                this.$emit('changeValue', this.realValue)
            }
        },
    },
}
</script>

<template>
    <div class="range-field">
        <slot name="beforeInput"> </slot>
        <div class="inputs">
            <StringField
                name="min"
                :value="realValue[0]"
                placeholder="от"
                type="number"
                @changeValue="value => setValue(value, 'min')"
            />
            -
            <StringField
                name="max"
                placeholder="до"
                type="number"
                :value="realValue[1]"
                @changeValue="value => setValue(value, 'max')"
            />
        </div>
    </div>
</template>
<style>
.range-field {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.inputs {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    gap: 12px;
    align-items: center;
}
.inputs input.field-input {
    width: 67px;
}
</style>

<script>
import InputPropsMixin from './help/props/InputPorpsMixin'

export default {
    mixins: [InputPropsMixin],
    emits: ['changeValue'],
    data() {
        return {
            minValue: this.value[0],
            maxValue: this.value[1],
        }
    },
    computed: {
        realValue() {
            return [this.minValue, this.maxValue]
        }
    },
    methods: {
        setValue(value, type) {
            this[`${type}Value`] = value
            if (this.realValue[0]!== null && this.realValue !== null) {
                this.$emit('changeValue', this.realValue)
            }
        },
    },
}
</script>

<template>
    <slot name="beforeInput"> </slot>
    <div class="fieldSwitch" :class="{ switched: realValue, disabled: disabled, hasText }">
        <label>
            <input
                type="checkbox"
                :disabled="disabled"
                :checked="realValue"
                @change="changeValue"
                :value="realValue"
                hidden
            />
            <span :class="{ mark: hasMark, text: hasText }"></span>
            <span class="mark-text"> {{ text }}</span>
        </label>
    </div>
</template>

<script>
export default {
    props: {
        value: { type: Boolean, default: () => false },
        activeText: { type: [String, Number], default: null },
        inactiveText: { type: [String, Number], default: null },
        hasMark: { type: Boolean, default: () => true },
        disabled: { type: Boolean, default: () => false },
        name: { type: String, default: () => '' },
    },
    emits: ['changeValue'],
    data() {
        return {
            focused: false,
            realValue: false,
        }
    },
    watch: {
        value() {
            this.realValue = this.value
        },
    },
    computed: {
        text() {
            if (this.hasText) return this.realValue ? this.activeText : this.inactiveText
            return this.realValue ? 'да' : 'нет'
        },
        hasText() {
            return this.activeText && this.inactiveText
        },
    },
    methods: {
        changeValue(e) {
            this.$emit('changeValue', (this.realValue = e.target.checked), this.name)
        },
    },
    created() {
        this.realValue = this.value
    },
}
</script>

<template>
    <div class="field fieldString">
        <slot name="beforeInput" v-bind="slotProps"></slot>

        <input
            class="field-input"
            :class="isValid ? 'valid' : 'invalid'"
            :type="type"
            :disabled="disabled"
            :readonly="readonly"
            :placeholder="placeholder"
            :size="size"
            :name="name"
            :min="min"
            :max="max"
            :autofocus="autofocus"
            v-model="realValue"
            @input="onInput"
            @focus="onFocus"
            @blur="onBlur"
        />
        <slot name="afterInput" v-bind="slotProps">
            <i
                v-if="realValue !== '' && focused && hasClearnBtn"
                class="icon icon-clear"
                @mousedown="clear"
            ></i>
        </slot>
    </div>
</template>

<script>
import InputPropsMixin from './help/props/InputPorpsMixin'

export default {
    mixins: [InputPropsMixin],
    data() {
        return {
            focused: false,
            realValue: this.value || '',
        }
    },
    watch: {
        value() {
            this.realValue = this.value
        },
    },
    computed: {
        slotProps() {
            return {
                value: this.realValue,
                focused: this.focused,
                hasClearnBtn: this.hasClearnBtn,
                clear: this.clear,
            }
        },
    },
    methods: {
        onFocus() {
            this.focused = true
            this.$emit('onFocus')
        },
        onBlur() {
            this.focused = false
            this.$emit('onBlur')
        },
        onInput() {
            if (this.afterInputFormat) {
                this.realValue = this.afterInputFormat(this.realValue)
            }
            this.$emit('changeValue', this.realValue, this.name)
        },
        clear(autofocus = true) {
            this.realValue = ''
            this.onInput()
            // Автофокус с таймаутом, чтобы перебить дефолтный автофокус
            autofocus && setTimeout(() => this.focus())
        },
        focus() {
            // Автофокус с таймаутом, чтобы перебить дефолтный автофокус
            this.$el.click()
                setTimeout(() => {
                    this.$el.querySelector('.field-input').focus()
            })
        },
    },
    created() {
        this.realValue = this.value
    },
}
</script>

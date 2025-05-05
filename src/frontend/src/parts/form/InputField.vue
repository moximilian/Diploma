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
            maxlength="64"
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
        checkSQLInjection(input) {
            // Default check for SQL Injection
            if (typeof input !== 'string') {
                return input
            }
            const value = input
                .replace(/[\0\x08\x09\x1a\n\r"'\\%]/g, char => {
                    // Экранируем специальные символы
                    const replacements = {
                        '\0': '\\0',
                        '\x08': '\\b',
                        '\x09': '\\t',
                        '\x1a': '\\z',
                        '\n': '\\n',
                        '\r': '\\r',
                        '"': '',
                        "'": '',
                        '\\\\': '',
                        '%': '\\%',
                    }
                    return replacements[char] || ''
                })
                .replace(
                    /(\b(union|select|insert|update|delete|drop|alter|create|exec|shutdown|--|#|\/\*|\*\/)\b)/gi,
                    ''
                )
            return value
        },
        onInput() {
            this.realValue = this.checkSQLInjection(this.realValue)
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

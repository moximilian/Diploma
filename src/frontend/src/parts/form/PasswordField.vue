<template>
    <div class="fieldPassword field">
        <slot name="beforeInput"></slot>
        <input
            class="field-input"
            :type="type"
            :disabled="disabled"
            :placeholder="placeholder"
            :name="name"
            v-model="realValue"
            @input="onInput"
            @focus="focused = true"
            @blur="focused = false"
        />
        <i
            v-if="realValue !== '' && focused"
            class="icon icon-show"
            title="Show password"
            @mousedown="changeHide"
        ></i>
    </div>
</template>

<script>
import FieldPropsMixin from './help/props/FieldPropsMixin'
export default {
    mixins: [FieldPropsMixin],
    data() {
        return {
            focused: false,
            isHide: true,
            realValue: '',
        }
    },
    computed: {
        type() {
            return this.isHide ? 'password' : 'text'
        },
    },
    methods: {
        onInput() {
            this.$emit('changeValue', this.realValue, this.name)
        },
        changeHide() {
            this.isHide = !this.isHide
            setTimeout(() => {
                this.$el.click()
                this.$el.querySelector('.field-input').focus()
            })
        },
    },
}
</script>

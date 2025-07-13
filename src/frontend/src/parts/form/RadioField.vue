<template>
    <div class="fieldRadio">
        <slot name="beforeInput"> </slot>
        <label
            v-for="(val, key) in options"
            :key="key"
            :class="{ selected: isSelected(key, val), disabled: disabled }"
        >
            <input
                :ref="'Input' + key"
                :type="inputType"
                :disabled="disabled"
                :checked="isSelected(key, val)"
                :value="optionKey(key, val)"
                hidden
                @change="changeRadio(key, val)"
            />
            <span class="mark" :class="inputType"></span>
            <span class="fieldRadio-text">{{ showValue(val) }}</span>
            <div v-if="hasChild" class="fieldRadio-child">
                <slot
                    name="child"
                    v-bind="{ value: val, key, options, isSelected: isSelected(key, val) }"
                ></slot>
            </div>
        </label>
    </div>
</template>

<script>
import SelectMixin from './help/SelectMixin.js'
export default {
    mixins: [SelectMixin],
    computed: {
        inputType() {
            return this.multiple ? 'checkbox' : 'radio'
        },
        hasChild() {
            return !!this.$slots['child']
        },
    },
    methods: {
        changeRadio(key, val) {
            this.onChange(key, val)
            this.$refs['Input' + key].checked = this.isSelected(key, val)
        },
    },
}
</script>

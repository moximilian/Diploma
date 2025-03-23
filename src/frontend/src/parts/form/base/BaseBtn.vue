<template>
    <button class="base-btn" :class="{ disabled, outline, inactive, special }" @click="clickBtn">
        <slot>{{ $t(`buttons.${value}`, value) }}</slot>
    </button>
</template>
<script>
export default {
    emits: ['click'],
    props: {
        value: { type: String, default: () => '' },
        disabled: { type: Boolean, default: () => false },
        outline: { type: Boolean, default: () => false },
        inactive: { type: Boolean, default: () => false },
        special: { type: Boolean, default: () => false },
    },
    methods: {
        clickBtn(e) {
            !this.disabled && this.$emit('click', e)
        },
    },
}
</script>

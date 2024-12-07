<template>
    <button class="base-btn" :class="{ disabled }" @click="clickBtn">
        <slot>{{ $t(`buttons.${value}`, value) }}</slot>
    </button>
</template>
<script>
export default {
    emits: ['click'],
    props: {
        value: { type: String, default: () => '' },
        disabled: { type: Boolean, default: () => false },
    },
    methods: {
        clickBtn() {
            !this.disabled && this.$emit('click')
        },
    },
}
</script>

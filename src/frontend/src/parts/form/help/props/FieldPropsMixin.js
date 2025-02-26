export default {
    props: {
        value: { type: [Array, Object, Number, String, Boolean], default: null },
        name: { type: [Array, String], default: null },
        placeholder: { type: String, default: null },
        title: { type: String, default: null },
        autofocus: { type: Boolean, default: () => false },
        disabled: { type: Boolean, default: () => false },
        afterInputFormat: { type: Function, default: null },
        isResetDisabled: { type: Boolean, default: () => false },
        isValid: { type: Boolean, default: () => true },
    },
    emits: ['changeValue'],
    directives: {
        focus: {
            mounted(el, binding) {
                binding.value && setTimeout(el.focus, 100)
            },
        },
    },
}

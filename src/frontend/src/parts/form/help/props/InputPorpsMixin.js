import FieldPropsMixin from './FieldPropsMixin'
export default {
    mixins: [FieldPropsMixin],
    props: {
        type: { type: String, default: () => 'text' },
        readonly: { type: Boolean, default: () => false },
        size: { type: Number, default: null },
        hasClearnBtn: { type: Boolean, default: true },
        min: { type: Number, default: null },
        max: { type: Number, default: null },
    },
    emits: ['onFocus', 'onBlur'],
}
